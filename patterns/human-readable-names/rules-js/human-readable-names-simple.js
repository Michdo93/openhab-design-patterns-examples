rules.JSRule({
  name: "Menschenlesbarer Name (einfach)",
  triggers: [triggers.ItemStateChangeTrigger("MyItem")],
  execute: (event) => {
    let name = actions.Transformation.transform("MAP", "admin.map", "MyItem");
    if (!name) name = "MyItem";

    console.log(name + " ist jetzt " + items.getItem("MyItem").state);
  }
});
