from bpy.types import NodeTree, Node, NodeSocket, NodeSocketString, NodeReroute
from nodeitems_utils import NodeCategory, NodeItem
import bpy
import nodeitems_builtins
import nodeitems_utils

class BnhelaNodeTree(NodeTree):
    bl_label = "Bnhela Node Tree"
    bl_icon = "EVENT_B"














class BnhelaNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'BnhelaNodeTree'



node_categories = [
    BnhelaNodeCategory(
        'GENERIC',
        "Basic",
        items=[
        ]
    ),

    BnhelaNodeCategory(
        'LAYOUT',
        "Layout",
        items=[
            NodeItem("NodeFrame"),
            NodeItem("NodeReroute"),
        ]
    )
]

classes = (
    BnhelaNodeTree,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('BNHELA_NODES', node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories('BNHELA_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    try:
        nodeitems_utils.unregister_node_categories('BNHELA_NODES')
    except:
        print('Keine Panik auf der Titanic')

    register()
