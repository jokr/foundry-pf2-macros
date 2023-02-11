async function createSource(effect) {
  const source = (await fromUuid(effect)).toObject();
  source.flags = mergeObject(source.flags ?? {}, {
    core: { sourceId: effect },
  });
  return source;
}

function hasEffect(actor, effect) {
  return actor.itemTypes.effect.find(
    (e) => e.flags.core?.sourceId === effect
  );
}

async function toggleEffect(actors, effect) {
  const source = await createSource(effect);
  for (const actor of actors) {
    const existing = hasEffect(actor, effect);
    if (existing) {
      await existing.delete();
    } else {
      await actor.createEmbeddedDocuments("Item", [source]);
    }
  }
}

async function addEffect(actors, effect) {
  const source = await createSource(effect);
  for (const actor of actors) {
    const existing = hasEffect(actor, effect);
    if (!existing) {
      await actor.createEmbeddedDocuments("Item", [source]);
    }
  }
}

async function removeEffect(actors, effect) {
  const source = await createSource(effect);
  for (const actor of actors) {
    const existing = hasEffect(actor, effect);
    if (existing) {
      await existing.delete();
    }
  }
}

/**
 * This macro applies the "Scout" effect to the character doing
 * the scouting and then applies the "Scouting" effect to the
 * entire party which grants the +1 circumstance bonus to initiative
 * rolls.
 */
async function runScouting() {
  const actors = canvas.tokens.controlled.flatMap((token) => token.actor ?? []);
  if (actors.length === 0 && game.user.character)
    actors.push(game.user.character);
  if (actors.length === 0) {
    const message = game.i18n.localize("PF2E.ErrorMessage.NoTokenSelected");
    return ui.notifications.error(message);
  }

  /**
   * This is a manually created effect to keep track which characters
   * does the Scout exploration activity. Create this in your Compendium
   * and then replace the ID here.
   */
  const SCOUT_UUID = "Item.eyUmSXjpO5WPRW7c"; // Scout
  await toggleEffect(actors, SCOUT_UUID);
  const isScouting = actors.find(a => hasEffect(a, SCOUT_UUID));

  const allPlayers = canvas.tokens.placeables
    .filter((t) => t.actor.isOfType("character"))
    .flatMap((t) => t.actor);

  const SCOUTING_UUID = "Compendium.pf2e.other-effects.EMqGwUi3VMhCjTlF"; // Scouting
  if (isScouting) {
    await addEffect(allPlayers, SCOUTING_UUID);
  } else {
    await removeEffect(allPlayers, SCOUTING_UUID);
  }
}

await runScouting();
