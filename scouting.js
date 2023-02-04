async function applyEffect(actors, effect) {
  const source = (await fromUuid(effect)).toObject();
  source.flags = mergeObject(source.flags ?? {}, {
    core: { sourceId: effect },
  });
  for (const actor of actors) {
    const existing = actor.itemTypes.effect.find(
      (e) => e.flags.core?.sourceId === effect
    );
    if (existing) {
      await existing.delete();
    } else {
      await actor.createEmbeddedDocuments("Item", [source]);
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
  await applyEffect(actors, SCOUT_UUID);

  const allPlayers = canvas.tokens.placeables
    .filter((t) => t.actor.isOfType("character"))
    .flatMap((t) => t.actor);

  const SCOUTING_UUID = "Compendium.pf2e.other-effects.EMqGwUi3VMhCjTlF"; // Scouting
  await applyEffect(allPlayers, SCOUTING_UUID);
}

await runScouting();
