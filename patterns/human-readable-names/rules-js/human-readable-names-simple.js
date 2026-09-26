rules.JSRule({
  name: "Human-readable name (simple)",
  triggers: [triggers.ItemStateChangeTrigger("MyItem")],
  execute: (event) => {
    let name = actions.Transformation.transform("MAP", "admin.map", "MyItem");
    if (!name) name = "MyItem";

    console.log(name + " is now " + items.getItem("MyItem").state);
  }
});
