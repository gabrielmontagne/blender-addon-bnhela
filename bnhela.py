from bpy.props import StringProperty
from bpy.types import NodeTree, Node, NodeSocket, NodeSocketString, NodeReroute
from functools import reduce
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

def find_outputs(acc, socket):


    sockets = [l.to_socket for l in socket.links]

    for socket in sockets:
        if socket.node.bl_idname == 'NodeReroute':
            print(' ∵ ∴ reroute', socket)
            acc += find_outputs(acc, socket)
        else:
            print('last stop', socket)
            acc.append(socket)

    return acc

def collate(acc, socket):

    print('collate for', socket)

    node = socket.node

    if node.bl_idname == 'NodeReroute':
        return reduce(collate, [l.to_socket for l in node.outputs[0].links], acc)

    return acc + [socket]

def get_all_outputs(socket):
    return reduce(collate, [l.to_socket for l in socket.links], [])

class BnhelaNodeTree(NodeTree):
    bl_label = BNT
    bl_icon = "EVENT_B"

    def update(self):
        print('\n' * 2, '=========== Node tree update')

class BnhelaEagerSocket():
    def on_name_update(self, context):

        if not self.is_output:
            return

        # other = get_other_socket(self)

        others = get_all_outputs(self)

        if others:
            print('others, result\n .', '\n . '.join([o.name for o in others]))
        else:
            print('…')

        for other in others:
            if other.bl_idname != self.bl_idname:
                return

            other.payload = self.payload
            other.node.update()

    payload: StringProperty('Name', update=on_name_update, default='')

    def draw(self, context, layout, node, text):
        layout.label(text=self.name.lower() + ' ' + self.payload)

class BnhelaCharacterSocket(BnhelaEagerSocket, NodeSocket):

    bl_label = 'Bnhela Character Socket'

    def draw_color(self, context, node):
        return (0.6, 0.0, 0.0, 1.0)

class BnhelaLocationSocket(BnhelaEagerSocket, NodeSocket):

    bl_label = 'Bnhela Character Socket'

    def draw_color(self, context, node):
        return (0.6, 0.0, 0.6, 1.0)


class BnhelaNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == BNT


class BnhelaLocationNode(Node, BnhelaNode):

    bl_label = "Location Node"
    bl_icon = 'VIEW_PERSPECTIVE'

    def on_payload_update(self, context):
        self.update()

    payload: StringProperty(update=on_payload_update)

    def draw_buttons(self, context, layout):
        layout = layout
        layout.prop(self, 'payload', text='Namε')

    def init(self, context):
        self.outputs.new('BnhelaLocationSocket', 'Name')

    def update(self):
        name_socket = self.outputs['Name']
        name_socket.payload = self.payload

    def draw_label(self):
        return '{} - λ'.format(self.payload)


class BnhelaCharacterNode(Node, BnhelaNode):

    bl_label = "Character Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    def on_payload_update(self, context):
        self.update()

    payload: StringProperty(update=on_payload_update)

    def draw_buttons(self, context, layout):
        layout = layout
        layout.prop(self, 'payload', text='Namε')

    def init(self, context):
        self.outputs.new('BnhelaCharacterSocket', 'Name')

    def update(self):
        name_socket = self.outputs['Name']
        name_socket.payload = self.payload

    def draw_label(self):
        return '{} - χ'.format(self.payload)


class BnhelaSceneNode(Node, BnhelaNode):

    bl_label = "Scene Node"
    bl_icon = 'VIEW_CAMERA'

    time_specifier = [
        ("DAY", "DAY", "", 0),
        ("NIGHT", "NIGHT", "", 1)
    ]

    day_or_night: bpy.props.EnumProperty(
        name="Time",
        items=time_specifier,
        default='DAY',
    )

    location_specifier = [
        ("INT.", "INT.", "", 0),
        ("EXT.", "EXT.", "", 1),
        ("INT./EXT.", "INT./EXT.", "", 2)
    ]

    int_or_ext: bpy.props.EnumProperty(
        name="Location",
        description="YY",
        items=location_specifier,
        default='INT.',
    )

    char_titles = [
        'MC',
        'OP',
        'WC'
    ]

    scene_index: bpy.props.IntProperty(name='Scene index', min=0)

    def init(self, context):
        self.width = 200

        self.inputs.new('BnhelaLocationSocket', 'Location')

        for char_title in self.char_titles:
            self.inputs.new('BnhelaCharacterSocket', char_title)
            self.outputs.new('BnhelaCharacterSocket', char_title)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'int_or_ext')
        layout.prop(self, 'day_or_night')
        layout.prop(self, 'scene_index')

    def draw_label(self):
        return '{:03d}. {} - {}'.format(self.scene_index, self.int_or_ext, self.day_or_night)

    def update(self):
        print('Scene node update', self)

        for char_title in self.char_titles:
            input = self.inputs[char_title]
            output = self.outputs[char_title]

            if not input.is_linked:
                input.payload = ''

            output.payload = input.payload








#####################################################################

classes = (
    BnhelaNodeTree,
    BnhelaCharacterNode,
    BnhelaLocationNode,
    BnhelaSceneNode,
    BnhelaCharacterSocket,
    BnhelaLocationSocket,
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
            NodeItem("BnhelaLocationNode"),
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
