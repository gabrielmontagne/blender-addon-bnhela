import bpy
import nodeitems_builtins
from bpy.types import NodeTree, Node, NodeSocket, NodeSocketString
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

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

    character_name: bpy.props.StringProperty(name='Name', default='MOTOKO')

    def init(self, context):
        self.outputs.new('NodeSocketString', 'Name')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'character_name')

class AnhelaSceneNode(Node, AnhelaNode):
    bl_label = "Scene Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    time_specifier = [
        ("DAY", "DAY", "", 0),
        ("NIGHT", "NIGHT", "", 1)
    ]

    location_specifier = [
        ("INT", "INT.", "", 0),
        ("EXT", "EXT.", "", 1),
        ("INTEXT", "INT./EXT.", "", 1)
    ]

    day_or_night: bpy.props.EnumProperty(
        name="Time",
        description="XX",
        items=time_specifier,
        default='DAY',
    )

    int_or_ext: bpy.props.EnumProperty(
        name="Location",
        description="YY",
        items=location_specifier,
        default='INT',
    )

    def init(self, context):
        print('Scene node init')
        self.inputs.new('NodeSocketString', 'Character')
        self.inputs.new('NodeSocketString', 'Character')
        self.inputs.new('NodeSocketString', 'Character')
        self.inputs.new('NodeSocketString', 'Character')

        self.outputs.new('NodeSocketString', 'Character')
        self.outputs.new('NodeSocketString', 'Character')
        self.outputs.new('NodeSocketString', 'Character')
        self.outputs.new('NodeSocketString', 'Character')

    def update(self):
        print('Scene node update', self)

    def insert_link(self, link):
        print('Scene link', self, link)

    def copy(self, node):
        print('Scene copy', self, node)

    def free(self):
        print('Scene free', self)

    def draw_buttons(self, context, layout):
        print('Scene draw buttons', self, context, layout)
        layout.prop(self, 'int_or_ext')
        layout.prop(self, 'day_or_night')

    def draw_buttons_ext(self, context, layout):
        print('Scene draw buttons ext', self, context, layout)

    def draw_label(self):
        print('Scene label')

        return '{} - {}'.format(self.int_or_ext, self.day_or_night)

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
