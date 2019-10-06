import bpy
import nodeitems_builtins
from bpy.types import NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

print(nodeitems_builtins, '<<<')

class AnhelaNodeTree(NodeTree):
    bl_label = "Anhela Node Tree"
    bl_icon = "NODETREE"

class AnhelaNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == "AnhelaNodeTree"

class AnhelaNoteNode(Node, AnhelaNode):
    bl_label = "Note Node"
    bl_icon = 'TEXT'


class AnhelaNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'AnhelaNodeTree'


node_categories = [
    AnhelaNodeCategory(
        'GENERIC', 
        "Generic", 
        items=[NodeItem('AnhelaNoteNode')]
    )
]

classes = (
    AnhelaNodeTree,
    AnhelaNoteNode
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    nodeitems_utils.register_node_categories('ANHELA_NODES', node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories('ANHELA_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
