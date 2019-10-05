import bpy
import nodeitems_builtins
from bpy.types import NodeTree, Node, NodeSocket

print(nodeitems_builtins, '<<<')

class AnhelaNodeTree(NodeTree):
    bl_label = "Anhela Node Tree"
    bl_icon = "NODETREE"

classes = (
    AnhelaNodeTree,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
