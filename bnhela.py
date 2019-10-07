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
        print('Name updated', self.character_name)

    character_name: StringProperty('Name', update=on_name_update, default='')

    def draw_color(self, context, node):
        return (0.6, 0.0, 0.0, 1.0)

    def draw(self, context, layout, node, text):
        layout.label(text='..' + self.character_name + '--')


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
        print('Char node update', self.name)
        print('   ... out socket', self.outputs['Name'])


        name_socket = self.outputs['Name']
        other_socket = get_other_socket(name_socket)

        name_socket.character_name = self.character_name

        if not other_socket:
            print('No other socket, ciao!')
            return


        if name_socket.bl_idname != other_socket.bl_idname:
            print('Socket mismatch, ouch X-(')
            return

        other_socket.character_name = self.character_name

        other_socket.node.update()


class BnhelaSceneNode(Node, BnhelaNode):

    bl_label = "Scene Node"
    bl_icon = 'VIEW_CAMERA'

    char_titles = [
        'MC',
        'OP',
        'WC'
    ]

    def init(self, context):

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
