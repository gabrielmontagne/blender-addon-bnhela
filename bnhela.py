from bpy.props import StringProperty
from bpy.types import NodeTree, Node, NodeSocket, NodeSocketString, NodeReroute
from nodeitems_utils import NodeCategory, NodeItem
import bpy
import nodeitems_builtins
import nodeitems_utils

BNT = "Bnhela Node Tree"

def get_other_socket(socket):
    """
    Get next real upstream socket.
    Will return None if there isn't a another socket connect
    so no need to check socket.links

    From, https://blender.stackexchange.com/a/153909/19669
    """

    if not socket.is_linked:
        return None
    if not socket.is_output:
        other = socket.links[0].from_socket
    else:
        other = socket.links[0].to_socket

    if other.node.bl_idname == 'NodeReroute':
        if not socket.is_output:
            return get_other_socket(other.node.inputs[0])
        else:
            return get_other_socket(other.node.outputs[0])
    else:
        return other


class BnhelaNodeTree(NodeTree):
    bl_label = BNT
    bl_icon = "EVENT_B"

    def update(self):
        print('\n' * 2, '=========== Node tree update')

class BnhelaCharacterSocket(NodeSocket):

    bl_label = 'Bnhela Character Socket'

    def on_name_update(self, context):

        if not self.is_output:
            return

        other = get_other_socket(self)
        if not other:
            return

        other.character_name = self.character_name
        other.node.update()

    character_name: StringProperty('Name', update=on_name_update, default='')

    def draw_color(self, context, node):
        return (0.6, 0.0, 0.0, 1.0)

    def draw(self, context, layout, node, text):
        layout.label(text=self.name.lower() + '_ ' + self.character_name)


class BnhelaSlugTimeSocket(NodeSocket):

    bl_label = 'Bnhela Slut Time Socket'

    time_specifier = [
        ("DAY", "DAY", "", 0),
        ("NIGHT", "NIGHT", "", 1)
    ]

    day_or_night: bpy.props.EnumProperty(
        name="Time",
        items=time_specifier,
        default='DAY',
    )

    def draw(self, context, layout, node, text):
        layout.prop(self, 'day_or_night')

    def draw_color(self, context, node):
        return(0.0, 0.6, 0.0, 1.0)

class BnhelaSlugIntExtSocket(NodeSocket):

    bl_label = 'Bnhela Slut Int/Ext Socket'

    location_specifier = [
        ("INT", "INT.", "", 0),
        ("EXT", "EXT.", "", 1),
        ("INTEXT", "INT./EXT.", "", 1)
    ]

    int_or_ext: bpy.props.EnumProperty(
        name="Location",
        description="YY",
        items=location_specifier,
        default='INT',
    )

    def draw(self, context, layout, node, text):
        layout.prop(self, 'int_or_ext')

    def draw_color(self, context, node):
        return(0.0, 0.6, 0.6, 1.0)


class BnhelaNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == BNT


class BnhelaCharacterNode(Node, BnhelaNode):

    bl_label = "Character Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    def on_character_name_update(self, context):
        print('on character_name update (on node)', self, self.character_name)
        self.update()

    character_name: StringProperty(update=on_character_name_update)

    def draw_buttons(self, context, layout):
        layout = layout
        layout.prop(self, 'character_name', text='Namε')

    def init(self, context):
        self.outputs.new('BnhelaCharacterSocket', 'Name')

    def update(self):
        name_socket = self.outputs['Name']
        name_socket.character_name = self.character_name

    def draw_label(self):
        return self.character_name


class BnhelaSceneNode(Node, BnhelaNode):

    bl_label = "Scene Node"
    bl_icon = 'VIEW_CAMERA'

    char_titles = [
        'MC',
        'OP',
        'WC'
    ]

    def init(self, context):

        self.width = 200

        self.inputs.new('NodeSocketInt', '#')
        self.inputs.new('BnhelaSlugIntExtSocket', '')
        self.inputs.new('BnhelaSlugTimeSocket', '')

        for char_title in self.char_titles:
            self.outputs.new('BnhelaCharacterSocket', char_title)
            self.inputs.new('BnhelaCharacterSocket', char_title)

    def update(self):
        print('Scene node update', self)

        for char_title in self.char_titles:
            input = self.inputs[char_title]
            output = self.outputs[char_title]

            if not input.is_linked:
                input.character_name = ''

            output.character_name = input.character_name
















#####################################################################

classes = (
    BnhelaNodeTree,
    BnhelaCharacterNode,
    BnhelaSceneNode,
    BnhelaCharacterSocket,
    BnhelaSlugTimeSocket,
    BnhelaSlugIntExtSocket,
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
