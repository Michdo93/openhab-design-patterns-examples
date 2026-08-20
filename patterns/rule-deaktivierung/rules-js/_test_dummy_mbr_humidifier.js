// Reine Test-Hilfsdatei, um "rule-deaktivierung.js" testen zu koennen -
// im echten Einsatz waere das eure tatsaechliche Luftbefeuchter-Regel.
rules.JSRule({
  id: "mbr_humidifier",
  name: "MBR Humidifier (Test-Dummy)",
  triggers: [triggers.ItemCommandTrigger("DummyRuleTrigger")],
  execute: (event) => {
    // absichtlich leer
  }
});
