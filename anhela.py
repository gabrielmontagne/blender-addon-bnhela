import bpy
import nodeitems_builtins
from bpy.types import NodeTree, Node, NodeSocket, NodeSocketString
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

class AnhelaCharacterNode(Node, AnhelaNode):
    bl_label = "Character Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    def init(self, context):
        self.outputs.new('NodeSocketString', 'Name')

class AnhelaSceneNode(Node, AnhelaNode):
    bl_label = "Scene Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    def init(self, context):
        self.inputs.new('NodeSocketString', 'Character')
        self.inputs.new('NodeSocketString', 'Character')
        self.inputs.new('NodeSocketString', 'Character')
        self.inputs.new('NodeSocketString', 'Character')

        self.outputs.new('NodeSocketString', 'Character')
        self.outputs.new('NodeSocketString', 'Character')
        self.outputs.new('NodeSocketString', 'Character')
        self.outputs.new('NodeSocketString', 'Character')

class AnhelaNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'AnhelaNodeTree'

node_categories = [
    AnhelaNodeCategory(
        'GENERIC',
        "Anhela",
        items=[
            NodeItem('AnhelaNoteNode'),
            NodeItem('AnhelaCharacterNode'),
            NodeItem('AnhelaSceneNode')
        ]
    )
]

classes = (
    AnhelaNodeTree,
    AnhelaNoteNode,
    AnhelaCharacterNode,
    AnhelaSceneNode
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
    try:
        nodeitems_utils.unregister_node_categories('ANHELA_NODES')
    except:
        print('Keine Panik auf der Titanic')

    register()
