// Loads a scene written by tools/bbscene.py into Blockbench (run through the MCP execute_script).
// Body of `new Function("scenePath", <this file>)`: returns a short report.
function readText(path) {
  let text = null;
  Blockbench.read([path], { readtype: "text" }, (files) => {
    text = files[0].content;
  });
  return text;
}

const scene = JSON.parse(readText(scenePath));
newProject(Formats.bedrock);
Project.name = scene.name;
const report = { layers: [], animations: 0, shared_bones: 0, warnings: [] };
const gameName = {}; // group uuid -> bone name in the game
const layerGroups = {}; // geometry id -> uuids of the groups it created
window.mvDebug = { layerGroups, gameName, scene }; // for inspecting a loaded scene

scene.layers.forEach((layer, i) => {
  const oldCubes = new Set(Cube.all.map((c) => c.uuid));
  const oldGroups = new Set(Group.all.map((g) => g.uuid));
  const object = {
    description: {
      identifier: layer.geometry,
      texture_width: layer.texture_width,
      texture_height: layer.texture_height,
    },
    bones: layer.bones,
  };
  Codecs.bedrock.parseGeometry({ object }, { import_to_current_project: i > 0, switch_to_existing_tab: false });
  let tex = null;
  if (layer.texture) {
    tex = new Texture({ name: layer.texture.split("/").pop() }).fromPath(layer.texture).add(false);
    tex.uv_width = layer.texture_width;
    tex.uv_height = layer.texture_height;
  } else {
    report.warnings.push("no texture for " + layer.geometry);
  }
  const cubes = Cube.all.filter((c) => !oldCubes.has(c.uuid));
  if (tex) cubes.forEach((c) => c.applyTexture(tex, true));
  const groups = Group.all.filter((g) => !oldGroups.has(g.uuid));
  // Blockbench renames duplicated bones (head -> head2); remember the name the game uses.
  // Groups are created in the order of the file's bones: pair them by position. (Stripping digits is
  // wrong: a layer may have its own bone "body6" that Blockbench renames "body10".)
  const names = layer.bones.map((b) => b.name.toLowerCase());
  const byOrder = groups.length === names.length;
  if (!byOrder) report.warnings.push(layer.geometry + ": bone count differs, names guessed");
  groups.forEach((g, gi) => {
    let original = byOrder ? names[gi] : g.name.toLowerCase();
    if (!byOrder && !names.includes(original)) original = original.replace(/\d+$/, "");
    gameName[g.uuid] = original;
    if (layer.hidden.includes(original)) {
      g.visibility = false;
      g.forEachChild((c) => (c.visibility = false));
    }
  });
  layerGroups[layer.geometry] = groups.map((g) => g.uuid);
  report.layers.push({ geometry: layer.geometry, cubes: cubes.length, groups: groups.length });
});
Project.texture_width = scene.layers.length ? scene.layers[0].texture_width : 64;
Project.texture_height = scene.layers.length ? scene.layers[0].texture_height : 64;

// Animations: only the entity's, from vanilla and add-on files.
scene.animation_files.forEach((path) => {
  const content = readText(path);
  if (!content) return;
  try {
    const json = autoParseJSON(content, false);
    const wanted = {};
    Object.keys(json.animations || {}).forEach((k) => {
      if (scene.animations.includes(k)) wanted[k] = json.animations[k];
    });
    if (Object.keys(wanted).length) {
      Animator.loadFile({ path, content: JSON.stringify({ format_version: "1.8.0", animations: wanted }) });
    }
  } catch (e) {
    report.warnings.push("animations " + path.split("/").pop() + ": " + e);
  }
});

// In the game every geometry is animated by bone NAME: copy each animator to the layer bones
// that share the name (Blockbench only binds the first group with that name).
Animation.all.forEach((anim) => {
  Group.all.forEach((group) => {
    const animator = anim.animators[group.uuid];
    if (!animator || !animator.keyframes.length) return;
    Group.all
      .filter((other) => other !== group && gameName[other.uuid] === gameName[group.uuid])
      .forEach((other) => {
        const copy = anim.getBoneAnimator(other);
        if (copy.keyframes.length) return;
        copy.rotation_global = animator.rotation_global; // "relative_to": {"rotation": "entity"} (look_at_target)
        animator.keyframes.forEach((kf) => copy.addKeyframe(kf.getUndoCopy()));
        report.shared_bones++;
      });
  });
});
// Animations the entity runs in this state play together (pose/setup + whatever is selected).
Project.variable_placeholders = scene.placeholders || "";
Animation.all.forEach((a) => {
  a.playing = scene.active.includes(a.name);
});
report.always_playing = Animation.all.filter((a) => a.playing).map((a) => a.name);

// mvPose(name, time): show animation `name` at `time` together with the always-playing ones, then take
// a `screenshot`. (The MCP's preview_animation plays only one animation, so the pose/setup is lost.)
window.mvPose = function (name, time) {
  Modes.options.animate.select();
  const target = name ? Animation.all.find((a) => a.name === name) : null;
  if (name && !target) return "no animation " + name;
  if (target) target.select();
  Animation.all.forEach((a) => {
    a.playing = a === target || scene.active.includes(a.name);
  });
  Timeline.setTime(time || 0);
  Animator.preview();
  return Animation.all.filter((a) => a.playing).map((a) => a.name);
};
window.mvPose(null, 0);

// mvExportLayer(geometry): write the bones of one layer (with the edits made in Blockbench, and any group
// added under them) to tools/out/bb/<geometry>.export.json, with the bone names the game uses.
// Then: python -I tools/bbapply.py <geometry> puts them into the add-on's .geo.json.
const outDir = scenePath.replace(/[^/]*$/, "");
window.mvExportLayer = function (geometry) {
  const own = new Set(layerGroups[geometry] || []);
  if (!own.size) return "no layer " + geometry + "; layers: " + Object.keys(layerGroups).join(", ");
  let grew = true;
  while (grew) {
    grew = false;
    Group.all.forEach((g) => {
      if (!own.has(g.uuid) && g.parent instanceof Group && own.has(g.parent.uuid)) {
        own.add(g.uuid);
        grew = true;
      }
    });
  }
  const bones = Group.all
    .filter((g) => own.has(g.uuid))
    .map((g) => {
      const bone = Codecs.bedrock.compileGroup(g);
      bone.name = gameName[g.uuid] || g.name;
      if (g.parent instanceof Group) bone.parent = gameName[g.parent.uuid] || g.parent.name;
      return bone;
    });
  const path = outDir + geometry + ".export.json";
  Blockbench.writeFile(path, { content: JSON.stringify({ geometry, bones }, null, 1), savetype: "text" });
  return { bones: bones.length, path };
};

// mvMeasure(animations?, fractions?): for every cube of every layer (all layers but the first, the base),
// where it would be if it were glued to the base bone with the same name, vs. where it really is, at
// several moments of each animation. Returns the worst separation in pixels per layer.
window.mvMeasure = function (names, fractions) {
  fractions = fractions || [0.125, 0.375, 0.625, 0.875];
  const base = scene.layers.length ? scene.layers[0].geometry : null;
  const baseByName = {};
  (layerGroups[base] || []).forEach((uuid) => {
    const g = Group.all.find((x) => x.uuid === uuid);
    if (g && !baseByName[gameName[uuid]]) baseByName[gameName[uuid]] = g;
  });
  const anchorOf = (el) => {
    let p = el.parent;
    while (p instanceof Group) {
      const b = baseByName[gameName[p.uuid]];
      if (b && b !== p) return [p, b];
      p = p.parent;
    }
    return null;
  };
  const probes = [];
  const unanchored = {};
  Object.keys(layerGroups).forEach((geo) => {
    if (geo === base) return;
    const own = new Set(layerGroups[geo]);
    Cube.all.forEach((c) => {
      if (!(c.parent instanceof Group) || !own.has(c.parent.uuid)) return;
      if (c.visibility === false) return;
      const a = anchorOf(c);
      if (!a) unanchored[geo] = (unanchored[geo] || 0) + 1;
      else probes.push({ geo, cube: c, layerBone: a[0], baseBone: a[1] });
    });
  });
  const update = () => Canvas.scene.updateMatrixWorld(true);
  window.mvPose(null, 0);
  update();
  probes.forEach((p) => {
    const rest = p.cube.getWorldCenter();
    p.local = rest.clone().applyMatrix4(new THREE.Matrix4().copy(p.baseBone.mesh.matrixWorld).invert());
  });
  const worst = {};
  // default: what an adult can run (bbscene excludes baby-only animations; skins never apply to babies)
  const pool = names && names.length ? names : scene.adult_animations || Animation.all.map((a) => a.name);
  const anims = pool.filter((n) => !scene.active.includes(n));
  anims.forEach((name) => {
    const anim = Animation.all.find((a) => a.name === name);
    if (!anim) return;
    const length = anim.length || 1;
    fractions.forEach((f) => {
      window.mvPose(name, f * length);
      update();
      probes.forEach((p) => {
        const expected = p.local.clone().applyMatrix4(p.baseBone.mesh.matrixWorld);
        const d = expected.distanceTo(p.cube.getWorldCenter());
        const w = worst[p.geo];
        if (!w || d > w.px) {
          worst[p.geo] = { px: Math.round(d * 100) / 100, bone: gameName[p.layerBone.uuid], animation: name, time: Math.round(f * length * 100) / 100 };
        }
      });
    });
  });
  window.mvPose(null, 0);
  Object.keys(layerGroups).forEach((geo) => {
    if (geo !== base && !worst[geo]) worst[geo] = { px: 0, bone: null, animation: null, time: null };
  });
  return { worst, unanchored, animations: anims.length, cubes: probes.length };
};
report.animations = Animation.all.length;
Canvas.updateAll();
return report;
