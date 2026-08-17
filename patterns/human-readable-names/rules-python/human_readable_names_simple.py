from openhab.actions import Transformation

name = Transformation.transform("MAP", "admin.map", "MyItem") or "MyItem"
