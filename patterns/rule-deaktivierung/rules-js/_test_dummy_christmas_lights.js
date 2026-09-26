// Reine Test-Hilfsdatei, um "rule-deaktivierung.js" testen zu können -
// im echten Einsatz wären das eure tatsächlichen Weihnachtslicht-Regeln.
rules.JSRule({
  id: "christmas_lights",
  name: "Christmas Lights (Test-Dummy)",
  triggers: [triggers.ItemCommandTrigger("DummyRuleTrigger")],
  execute: (event) => {
    // absichtlich leer
  }
});
