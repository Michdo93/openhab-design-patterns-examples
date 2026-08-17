rules.JSRule({
  name: "Is it cloudy outside?",
  triggers: [triggers.ItemStateChangeTrigger("vCloudiness")],
  execute: (event) => {
    const newState = parseFloat(items.getItem("vCloudiness").state) > 50 ? "ON" : "OFF";
    if (newState !== items.getItem("vIsCloudy").state) {
      items.getItem("vIsCloudy").postUpdate(newState);
    }
  }
});
