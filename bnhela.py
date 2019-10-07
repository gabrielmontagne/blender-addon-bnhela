from bpy.types import NodeTree, Node, NodeSocket, NodeSocketString, NodeReroute
from nodeitems_utils import NodeCategory, NodeItem
import bpy
import nodeitems_builtins
import nodeitems_utils

BNT = "Bnhela Node Tree"

class BnhelaNodeTree(NodeTree):
    bl_label = BNT
    bl_icon = "EVENT_B"

class BnhelaCharacterSocket(NodeSocket):

    bl_label = 'Bnhela Character Socket'

    def draw_color(self, context, node):
        return (0.6, 0.0, 0.0, 1.0)

    def draw(self, context, layout, node, text):
        layout.label(text=text)




class BnhelaNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == BNT


class BnhelaCharacterNode(Node, BnhelaNode):

    bl_label = "Character Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    def init(self, context):
        self.outputs.new('BnhelaCharacterSocket', 'Name')



class BnhelaSceneNode(Node, BnhelaNode):

    bl_label = "Scene Node"
    bl_icon = 'VIEW_CAMERA'

    def init(self, context):
        self.inputs.new('BnhelaCharacterSocket', 'Main Character')
        self.inputs.new('BnhelaCharacterSocket', '2nd Character')
        self.inputs.new('BnhelaCharacterSocket', '3rd Character')















#####################################################################

classes = (
    BnhelaNodeTree,
    BnhelaCharacterNode,
    BnhelaSceneNode,
    BnhelaCharacterSocket,
)


class BnhelaNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'BnhelaNodeTree'



node_categories = [
    BnhelaNodeCategory(
        'GENERIC',
        "Basic",
        items=[
            NodeItem("BnhelaCharacterNode"),
            NodeItem("BnhelaSceneNode"),
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
