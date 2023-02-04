async function applyEffectOrRefresh(actors, effect) {
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
    }
    await actor.createEmbeddedDocuments("Item", [source]);
  }
}

/**
 * This macro applies the Inspire Courage effect to the party. This
 * is a broad simplification, as technically the aura needs Line of
 * Effect and has a limit of 60 feet. But running this as an aura does
 * not work for some strange reason...
 */
async function runInspireCourage() {
  const allPlayers = canvas.tokens.placeables
    .filter((t) => t.actor.isOfType("character"))
    .flatMap((t) => t.actor);

  const INSPIRE_COURAGE_UUID = "Compendium.pf2e.spell-effects.beReeFroAx24hj83";
  await applyEffectOrRefresh(allPlayers, INSPIRE_COURAGE_UUID);
}

await runInspireCourage();
