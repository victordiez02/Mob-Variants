// Test harness run by tools/bdstest.py on a Bedrock Dedicated Server.
// Spawns every mob COUNT times (fires minecraft:entity_spawned like a natural spawn), reads its mv:*
// properties and prints one "MVTEST {json}" line per mob, then "MVTEST-DONE".
// config.js is written by bdstest.py: export const MOBS = [{ id, props: [...] }], COUNT, BOSS_COUNT, BOSSES.
import { world, system } from "@minecraft/server";
import { MOBS, COUNT, BOSS_COUNT, BOSSES, Y } from "./config.js";

// Y (bdstest --y, default 64 = surface): filters like is_altitude < 30 (zombie miners) need --y 10.
const LOC = { x: 0.5, y: Y, z: 0.5 };

function log(obj) {
  console.warn("MVTEST " + JSON.stringify(obj));
}

async function waitForChunk(dim) {
  for (let i = 0; i < 120; i++) {
    try {
      dim.spawnEntity("minecraft:armor_stand", LOC).remove();
      return true;
    } catch (e) {
      await system.waitTicks(10);
    }
  }
  return false;
}

async function testMob(dim, mob) {
  const n = BOSSES.includes(mob.id) ? BOSS_COUNT : COUNT;
  const counts = {};
  for (const p of mob.props) counts[p] = {};
  const spawned = [];
  let firstError = null;
  for (let i = 0; i < n; i++) {
    try {
      spawned.push(dim.spawnEntity(mob.id, LOC));
    } catch (e) {
      firstError = firstError ?? String(e);
    }
    if (i % 25 === 24) await system.waitTicks(1);
  }
  await system.waitTicks(3);
  let read = 0;
  for (const e of spawned) {
    if (!e.isValid) continue;
    read++;
    for (const p of mob.props) {
      let v;
      try {
        v = e.getProperty(p);
      } catch (err) {
        v = "error";
      }
      const key = String(v);
      counts[p][key] = (counts[p][key] ?? 0) + 1;
    }
    try {
      e.remove();
    } catch (err) {
      // already gone
    }
  }
  log({ mob: mob.id, spawned: spawned.length, read, counts, error: firstError });
}

async function main() {
  const dim = world.getDimension("overworld");
  try {
    dim.runCommand("tickingarea add circle 0 0 0 2 mvtest true");
  } catch (e) {
    // exists already
  }
  if (!(await waitForChunk(dim))) {
    log({ error: "spawn chunk never loaded" });
  } else {
    for (const mob of MOBS) {
      await testMob(dim, mob);
      await system.waitTicks(2);
    }
  }
  console.warn("MVTEST-DONE");
}

world.afterEvents.worldLoad.subscribe(() => {
  system.run(() => {
    main().catch((e) => {
      log({ error: String(e) });
      console.warn("MVTEST-DONE");
    });
  });
});
