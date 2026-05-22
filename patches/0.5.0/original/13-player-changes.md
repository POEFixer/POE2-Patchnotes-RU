## Player Changes

- Bleed damage on players is no longer increased while the player is moving. This change does not affect bleeds players apply to monsters.
- Your maximum Runic Ward is now added to your starting Honour when beginning a Trial of the Sekhemas.
- The "Defences" keyword is no longer in use. Existing uses of the word "Defences" now explicitly refer to "Armour, Evasion and Energy Shield" to make it more clear that these modifiers do not apply to Runic Ward, Resistances, Block, or other forms of protection. This is purely a description change.
- Only a single Leech instance per resource (Life, Mana, or Energy Shield) can apply at a time. When multiple Leech instances are active, only the one with the highest recovery rate will recover you until it expires, after which the next-highest recovery rate instance will apply.
- There is now a limit on the maximum amount of damage a hit can be considered to deal for Leech. Hits that deal less than 40,000 total damage are unaffected, but if a hit would deal more than 40,000 total damage, it is treated as dealing only 40,000 damage for purposes of Leech calculation. The values of each damage type in the hit are scaled down evenly to reach this limit. This means that extremely high-damage hits stop improving Leech past a certain point, but increasing your leech percentage will always increase the amount of the resource you are gaining.
- The formula for chance to Deflect has been adjusted to provide better scaling with investment into Deflection Rating, with a cap of 95% chance to Deflect (similar to chance to Evade being capped at 95%).
- The new chance to Deflect is = 150*(1 - A/(A + 0.12*D)), where A = attacker accuracy rating, and D = defender deflection rating. This makes for a linear path, that gets rewarded at higher investments.
- Parry, Shield Block and Resonating Shield no longer delay Heavy Stun buildup from decaying longer than expected.
- Melee Attacks can now only apply Splash Damage once per damaging area. Some Attacks create multiple damaging areas during use. For example, Whirling Assault creates multiple damaging areas around you as you move.
- When Minions are removed due to resources changing (such as weapon swapping), younger (newer) Minions are now prioritised for removal over older Minions to avoid wasting Minion cooldown abilities unnecessarily.
- Minions affected by Last Gasp Support or Tecrod's Revenge Lineage Support and Totems affected by the Unnamed Heartwood Oracle Notable Passive Skill can no longer die during the effect from taking further damage exceeding their Maximum Life.
- Stats worded as "when you collect a Remnant" no longer give you the benefits of these stats when an Ally shares the effects of a Remnant with you.
- Updated the name of the buff that Trinity grants to Affinity (as Resonance is the name of a Keystone passive skill). This is purely a description update.
- Archon Buffs are no longer inherently lost when you attack. This is now a property of Elemental Archon specifically.
[Return to top](#top)
