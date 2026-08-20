// Reine Test-Hilfsdatei, um "rule-deaktivierung.js" testen zu koennen -
// im echten Einsatz waeren das eure tatsaechlichen Weihnachtslicht-Regeln.
rules.JSRule({
  id: "christmas_lights",
  name: "Christmas Lights (Test-Dummy)",
  triggers: [triggers.ItemCommandTrigger("DummyRuleTrigger")],
  execute: (event) => {
    // absichtlich leer
  }
});
