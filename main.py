import random
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import sys
import os
from pathlib import Path

def resource_path(rel=''):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return Path(os.path.join(base, rel))

app = Ursina()

blocks = {
    'grass': {'texture': load_texture('grass'),'hand': load_texture('hgrass'), 'soundm': 'sound/grass_mine','soundp': 'sound/grass_mine'},
    'dirt':  {'texture': load_texture('dirt'), 'hand': load_texture('hdirt'), 'soundm': 'sound/dirt_mine','soundp': 'sound/dirt_place'},
    'stone': {'texture': load_texture('stone'), 'hand': load_texture('hstone'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'bedrock': {'texture': load_texture('bedrock'),'hand': load_texture('hbedrock'), 'soundm': 'sound/bedrock_mine','soundp': 'sound/stone_place'},
    'andesite': {'texture': load_texture('andesite'), 'hand': load_texture('handesite'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'coal_ore': {'texture': load_texture('coal_ore'), 'hand': load_texture('hcoal_ore'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'copper_ore': {'texture': load_texture('copper_ore'), 'hand': load_texture('hcopper_ore'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'gold_ore': {'texture': load_texture('gold_ore'), 'hand': load_texture('hgold_ore'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'granite': {'texture': load_texture('granite'), 'hand': load_texture('hgranite'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'gravel': {'texture': load_texture('gravel'), 'hand': load_texture('hgravel'),'soundm': 'sound/gravel_mine','soundp': 'sound/gravel_mine'},
    'sand': {'texture': load_texture('sand'), 'hand': load_texture('hsand'),'soundm': 'sound/sand_mine','soundp': 'sound/sand_mine'},
    'magma': {'texture': load_texture('magma'), 'hand': load_texture('hmagma'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'iron_ore': {'texture': load_texture('iron_ore'), 'hand': load_texture('hiron_ore'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'redstone_ore': {'texture': load_texture('redstone_ore'), 'hand': load_texture('hredstone_ore'),'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'emerald_ore': {'texture': load_texture('emerald_ore'), 'hand': load_texture('emerald_ore'), 'soundm': 'sound/stone_mine','soundp': 'sound/stone_place'},
    'wood': {'texture': load_texture('wood'), 'hand': load_texture('hwood'), 'soundm': 'sound/wood_mine', 'soundp': 'sound/wood_mine'},
    'leave': {'texture': load_texture('leave'), 'hand': load_texture('hleave'), 'soundm': 'sound/leave_mine', 'soundp': 'sound/leave_mine'},
}
mine_blk = {
    'stone': {'texture': load_texture('stone'), 'hand': load_texture('hstone'),'sound': 'sound/stone_mine',},
    'andesite': {'texture': load_texture('andesite'), 'hand': load_texture('handesite'),'sound': 'sound/andesite_mine'},
    'coal_ore': {'texture': load_texture('coal_ore'), 'hand': load_texture('hcoal_ore'),'sound': 'sound/coal_ore_mine'},
    'copper_ore': {'texture': load_texture('copper_ore'), 'hand': load_texture('hcopper_ore'),'sound': 'sound/copper_ore_mine'},
    'gold_ore': {'texture': load_texture('gold_ore'), 'hand': load_texture('hgold_ore'),'sound': 'sound/gold_ore_mine'},
    'granite': {'texture': load_texture('granite'), 'hand': load_texture('hgranite'),'sound': 'sound/granite_mine'},
    'gravel': {'texture': load_texture('gravel'), 'hand': load_texture('hgravel'),'sound': 'sound/gravel_mine'},
    'sand': {'texture': load_texture('sand'), 'hand': load_texture('hsand'),'sound': 'sound/sand_mine'},
    'magma': {'texture': load_texture('magma'), 'hand': load_texture('hmagma'),'sound': 'sound/magma_mine'},
    'iron_ore': {'texture': load_texture('iron_ore'), 'hand': load_texture('hiron_ore'),'sound': 'sound/iron_ore_mine'},
    'redstone_ore': {'texture': load_texture('redstone_ore'), 'hand': load_texture('hredstone_ore'),'sound': 'sound/redstone_ore_mine'},
    'emerald_ore': {'texture': load_texture('emerald_ore'), 'hand': load_texture('hemerald_ore'), 'sound': 'sound/stone_mine'},
    
    
}
mine_blk_list = ['stone','andesite','coal_ore','copper_ore','granite','gravel','sand','iron_ore','magma','gold_ore','redstone_ore','emerald_ore']


mine_blk_weights = [
    65,  
    10,  
    5,  
    4,   
    5,   
    6,  
    3,   
    0.9,   
    0.5,
    0.3,   
    0.2,   
    0.1
]

occupied_positions = set()
mined_positions = set()
gen_chunks = set()

def block(x,y,z,block):
   pos = (int(x),int(y),int(z))
   if pos not in occupied_positions and pos not in mined_positions :
       e =Entity(
        model='cube',
        scale=1,
        position = pos,
        texture= blocks[block]['texture'],
        collider='box'
       )
       e.is_block = True
       e.block = block                  
       occupied_positions.add(pos)

def chunk(x,y,z):
    if (x,y,z) in gen_chunks:
        return
    else:
        gen_chunks.add((x,y,z))
        for y_ in range(5):
          for z_ in range(5):
            for x_ in range(5):
                blk = random.choices(mine_blk_list, weights=mine_blk_weights, k=1)[0]
                pos = (x + x_ , y +y_ , z+ z_) 
                if pos not in occupied_positions and pos not in mined_positions :
                  e =Entity(
                     model='cube',
                     scale=1,
                     position = pos,
                     texture= mine_blk[blk]['texture'],
                     collider='box')
                  e.is_block = True
                  e.block = blk                 
                  occupied_positions.add(pos)


inventory = {}
blk_in_inven = []
selblk = 0

slot1bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(-0.225, 0.45,0.1),
    scale=0.05
)
slot2bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(-0.175, 0.45,0.1),
    scale=0.05
)
slot3bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=( -0.125, 0.45,0.1),
    scale=0.05
)
slot4bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(-0.075, 0.45,0.1),
    scale=0.05
)
slot5bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(-0.025, 0.45,0.1),
    scale=0.05
)
slot6bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.025, 0.45,0.1),
    scale=0.05
)
slot7bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.075, 0.45,0.1),
    scale=0.05
)
slot8bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.125, 0.45,0.1),
    scale=0.05
)
slot9bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.175, 0.45,0.1),
    scale=0.05
)
slot10bg = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.225, 0.45,0.1),
    scale=0.05
)

slot1 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(-0.225, 0.45),
    scale=0.042
)
slot2 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(-0.175, 0.45),
    scale=0.042
)
slot3 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=( -0.125, 0.45),
    scale=0.042
)
slot4 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(-0.075, 0.45),
    scale=0.042
)
slot5 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(-0.025, 0.45),
    scale=0.042
)
slot6 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(0.025, 0.45),
    scale=0.042
)
slot7 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(0.075, 0.45),
    scale=0.042
)
slot8 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(0.125, 0.45),
    scale=0.042
)
slot9 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(0.175, 0.45),
    scale=0.042
)
slot10 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.white,
    position=(0.225, 0.45),
    scale=0.042
)

slots = [slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10]

hand = Entity(
    parent=camera.ui,
    model='quad',
    scale= 0.8,
    position=(0.6, -0.35, 1),
    color = color.clear
)

    
Player = FirstPersonController(position = (0,15,0),scale=(0.7, 0.95, 0.7),)
def gen_plain(x ):
    pos_player = int(max(abs(Player.x),abs(Player.z)))
    for i in range(pos_player +x ):
        for y, tex in [(-7, 'bedrock'), (-1, 'dirt'), (0, 'grass')]:
            block(0,y,i,tex); block(i,y,i,tex); block(i,y,0,tex)
            block(i,y,-i,tex); block(0,y,-i,tex); block(-i,y,i,tex)
            block(-i,y,-i,tex); block(-i,y,0,tex)
            for x in range(i):
                block(x,y,i,tex); block(i,y,x,tex)
                block(x,y,-i,tex); block(-i,y,x,tex)
                block(-x,y,i,tex); block(i,y,-x,tex)
                block(-x,y,-i,tex); block(-i,y,-x,tex)

def gen_chunk():
    cx = (int(Player.x) // 5) * 5
    cz = (int(Player.z) // 5) * 5
    chunk(cx + 5, -6, cz + 5)
    chunk(cx - 5, -6, cz + 5)
    chunk(cx + 5, -6, cz - 5)
    chunk(cx - 5, -6, cz - 5)
    chunk(cx,     -6, cz + 5)
    chunk(cx,     -6, cz - 5)
    chunk(cx + 5, -6, cz    )
    chunk(cx - 5, -6, cz    )
    chunk(cx,     -6, cz    )

gen_plain(10)
gen_chunk()


Player.last_chunk = (0, 0)
def update():
    cx = (int(Player.x) // 5) * 5
    cz = (int(Player.z) // 5) * 5
    current_chunk = (cx, cz)

    if current_chunk != Player.last_chunk:
        gen_plain(10)
        gen_chunk()
        Player.last_chunk = current_chunk

    
    

    

def Tree():
    if not occupied_positions:
        return
    else:
        surface_positions = [pos for pos in occupied_positions if pos[1] == 0]
        if not surface_positions:
            return

        max_x = max(abs(pos[0]) for pos in surface_positions)
        max_z = max(abs(pos[2]) for pos in surface_positions)

        px, pz = int(Player.x), int(Player.z)

        tx = random.randint(min(px, max_x), max(px, max_x))
        tz = random.randint(min(pz, max_z), max(pz, max_z))
        th = 4
        for i in range(th+1):
            block(tx,1 +i,tz,'wood')
        block(tx , th , tz -1, 'leave')
        block(tx , th , tz -2, 'leave')
        block(tx  , th , tz+1 , 'leave')
        block(tx  , th , tz +2, 'leave')
        block(tx-1 , th , tz , 'leave')
        block(tx-2 , th , tz , 'leave')
        block(tx +1 , th , tz , 'leave')
        block(tx +2 , th , tz , 'leave')
        block(tx-1 , th , tz-2 , 'leave')
        block(tx-2 , th , tz-2 , 'leave')
        block(tx +1 , th , tz -2, 'leave')
        block(tx +2 , th , tz-2 , 'leave')
        block(tx-1 , th , tz-1 , 'leave')
        block(tx-2 , th , tz -1, 'leave')
        block(tx +1 , th , tz -1, 'leave')
        block(tx +2 , th , tz -1, 'leave')
        block(tx-1 , th , tz+1 , 'leave')
        block(tx-2 , th , tz +1, 'leave')
        block(tx +1 , th , tz +1, 'leave')
        block(tx +2 , th , tz +1, 'leave')
        block(tx-1 , th , tz +2, 'leave')
        block(tx-2 , th , tz +2, 'leave')
        block(tx +1 , th , tz +2, 'leave')
        block(tx +2 , th , tz+2, 'leave')
        block(tx ,th+1,tz-1,'leave')
        block(tx ,th+1,tz,'leave')
        block(tx ,th+1,tz+1,'leave')
        block(tx+1 ,th+1,tz-1,'leave')
        block(tx +1,th+1,tz,'leave')
        block(tx +1,th+1,tz+1,'leave')
        block(tx-1 ,th+1,tz-1,'leave')
        block(tx-1 ,th+1,tz,'leave')
        block(tx-1 ,th+1,tz+1,'leave')
        block(tx ,th+2,tz,'leave')
def Hand():
    if blk_in_inven:
        hand.texture = None 
        hand.color = color.clear
        hand.texture = blocks[blk_in_inven[selblk]]['hand']
        hand.visible = True
        hand.color = color.white
    else:
        hand.visible = False
        hand.alpha = 0.0
        
def reslots():
    for i, slot in enumerate(slots):
        if i < len(blk_in_inven):
            slot.texture = blocks[blk_in_inven[i]]['hand']
        else:
            slot.texture = None

w_held=False
w_timer = 0



def input(key):
    global selblk
    global w_timer, w_held
    
    if held_keys['w']:
        w_timer += time.dt
        if w_timer >= 1.5 and not w_held:
            w_held = True
            Tree()
    else:
        w_timer = 0
        w_held = False

    if held_keys['shift']:
        Player.camera_pivot.y = 2 - (held_keys['shift'])/2
        Player.speed = 3
    
    if key == 'scroll up' and len(blk_in_inven):
    
        selblk = (selblk + 1) % len(blk_in_inven)
        reslots()
        Hand()
    
    if key == 'scroll down' and len(blk_in_inven):
        
        selblk = (selblk - 1) % len(blk_in_inven)
        reslots()
        Hand()
        
    if key == 'left mouse down':
        entity =  mouse.hovered_entity
        entity = mouse.hovered_entity
        if entity and getattr(entity, 'is_block', False):
            pos = (int(entity.x), int(entity.y), int(entity.z))
            block = entity.block
            if block != 'bedrock' :
                occupied_positions.discard(pos)
                mined_positions.add(pos)
                destroy(entity)
                Audio(blocks[block]['soundm'],1,autoplay=True)
                if block not in inventory:
                    blk_in_inven.append(block)
                    inventory[block] = 1
                else:
                    inventory[block] += 1
                for i, slot in enumerate(slots):
                    if i < len(blk_in_inven) : 
                        slot.texture = blocks[blk_in_inven[i]]['hand'] 
                    else:
                        None
                reslots()
                Hand()
    if key=='right mouse down' :
        if not blk_in_inven:
           return
        entity = mouse.hovered_entity
        if entity and getattr(entity , 'is_block', False):
            pos = int(entity.x + mouse.normal.x),int(entity.y + mouse.normal.y),int(entity.z + mouse.normal.z)
            if pos not in occupied_positions :
                e = Entity(
                    model='cube',
                    scale=1,
                    position = pos ,
                    texture=blocks[blk_in_inven[selblk]]['texture'],
                    collider='box'
                )
                e.is_block = True
                e.block = blk_in_inven[selblk]
                occupied_positions.add(pos)
                mined_positions.discard(pos)
                Audio(blocks[blk_in_inven[selblk]]['soundp'] , 1 , autoplay=True)
                inventory[blk_in_inven[selblk]] -= 1
                if inventory[blk_in_inven[selblk]] == 0:
                    del inventory[blk_in_inven[selblk]]
                    blk_in_inven.pop(selblk)
                    slots[selblk].texture = None
                if blk_in_inven:
                    selblk = min(selblk, len(blk_in_inven) - 1)
                else:
                    selblk = 0
                for i, slot in enumerate(slots):
                    if i < len(blk_in_inven): 
                        slot.texture = blocks[blk_in_inven[i]]['hand'] 
                    else:
                        None
                
                reslots()
                Hand()

sky = Sky() 
sky = Sky(texture='sky_defult')



app.run()