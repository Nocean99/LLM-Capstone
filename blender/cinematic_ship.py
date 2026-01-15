import bpy
import math

# ============================================
# SETUP - Clear scene
# ============================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)
for block in bpy.data.images:
    if block.users == 0:
        bpy.data.images.remove(block)

print("Importing mesh...")

# ============================================
# IMPORT THE GLB MODEL
# ============================================
bpy.ops.import_scene.gltf(
    filepath=r"C:\Users\noahs\Desktop\ai experiments\blender\Meshy_AI_A_highly_detailed_or_0112213335_generate.glb"
)

imported_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
if not imported_objects:
    imported_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

bpy.ops.object.select_all(action='DESELECT')
for obj in imported_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = imported_objects[0]

if len(imported_objects) > 1:
    bpy.ops.object.join()

ship = bpy.context.active_object
ship.name = "Spaceship"

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
ship.location = (0, 0, 0)

max_dim = max(ship.dimensions)
if max_dim > 0:
    scale_factor = 5.0 / max_dim
    ship.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

print(f"Ship dimensions: {ship.dimensions}")

# ============================================
# SPACE BACKGROUND - Your image as environment
# ============================================

print("Setting up space background...")

world = bpy.data.worlds.new(name="Space_HDRI")
bpy.context.scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

# Load your background image
tex_coord = nodes.new('ShaderNodeTexCoord')
tex_coord.location = (-800, 0)

mapping = nodes.new('ShaderNodeMapping')
mapping.location = (-600, 0)
mapping.inputs['Rotation'].default_value = (0, 0, math.radians(0))

env_tex = nodes.new('ShaderNodeTexEnvironment')
env_tex.location = (-300, 0)
env_tex.image = bpy.data.images.load(r"C:\Users\noahs\Desktop\ai experiments\blender\space background.png")
env_tex.interpolation = 'Smart'

background = nodes.new('ShaderNodeBackground')
background.location = (0, 0)
background.inputs['Strength'].default_value = 1.0

output = nodes.new('ShaderNodeOutputWorld')
output.location = (300, 0)

links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], env_tex.inputs['Vector'])
links.new(env_tex.outputs['Color'], background.inputs['Color'])
links.new(background.outputs['Background'], output.inputs['Surface'])

# ============================================
# DRAMATIC SHADOW LIGHTING
# Key: Light from planet direction, rest in shadow
# ============================================

print("Setting up cinematic lighting...")

# Main light - simulating planet reflection / distant star
# Positioned to create dramatic shadows, coming from upper right rear
bpy.ops.object.light_add(type='SUN', location=(10, 10, 8))
key_light = bpy.context.active_object
key_light.name = "Planet_Light"
key_light.data.energy = 2.0  # Reduced for moodier look
key_light.data.color = (0.85, 0.9, 1.0)  # Slightly cool/blue to match space
key_light.data.angle = math.radians(0.5)  # Sharp shadows
key_light.rotation_euler = (math.radians(50), math.radians(20), math.radians(135))

# Very subtle fill - just to keep pure black from being flat
bpy.ops.object.light_add(type='AREA', location=(-8, -5, -2))
fill_light = bpy.context.active_object
fill_light.name = "Ambient_Fill"
fill_light.data.energy = 15  # Very low - just kissing the shadows
fill_light.data.color = (0.4, 0.45, 0.6)  # Cool blue ambient
fill_light.data.size = 10
fill_light.rotation_euler = (math.radians(120), 0, math.radians(-30))

# Subtle rim light - edge definition
bpy.ops.object.light_add(type='AREA', location=(-6, 6, 2))
rim_light = bpy.context.active_object
rim_light.name = "Rim_Light"
rim_light.data.energy = 80  # Subtle rim
rim_light.data.color = (0.6, 0.7, 0.9)  # Cold blue
rim_light.data.size = 3
rim_light.rotation_euler = (math.radians(70), 0, math.radians(-140))

# ============================================
# DARKEN/DESATURATE SHIP MATERIALS
# Make it grittier to match background
# ============================================

print("Adjusting ship materials for gritty look...")

for mat in ship.data.materials:
    if mat and mat.use_nodes:
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Find the output node
        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        if output_node and output_node.inputs['Surface'].links:
            # Get what's connected to output
            from_socket = output_node.inputs['Surface'].links[0].from_socket
            from_node = from_socket.node
            
            # Add HSV node to desaturate and darken
            hsv = nodes.new('ShaderNodeHueSaturation')
            hsv.location = (output_node.location.x - 200, output_node.location.y + 100)
            hsv.inputs['Saturation'].default_value = 0.7  # Reduce saturation
            hsv.inputs['Value'].default_value = 0.6  # Darken
            
            # Add color mix to add gritty overlay
            mix = nodes.new('ShaderNodeMixRGB')
            mix.location = (output_node.location.x - 400, output_node.location.y + 100)
            mix.blend_type = 'OVERLAY'
            mix.inputs['Fac'].default_value = 0.15
            mix.inputs['Color2'].default_value = (0.2, 0.22, 0.25, 1)  # Gritty blue-gray
            
            # Find base color input on principled BSDF
            if from_node.type == 'BSDF_PRINCIPLED':
                base_color_socket = from_node.inputs.get('Base Color')
                if base_color_socket:
                    # Darken and desaturate the base color
                    if base_color_socket.links:
                        orig_from = base_color_socket.links[0].from_socket
                        links.new(orig_from, mix.inputs['Color1'])
                        links.new(mix.outputs['Color'], hsv.inputs['Color'])
                        links.new(hsv.outputs['Color'], base_color_socket)
                    else:
                        # Static color - darken it
                        orig_color = list(base_color_socket.default_value)
                        base_color_socket.default_value = (
                            orig_color[0] * 0.5,
                            orig_color[1] * 0.5,
                            orig_color[2] * 0.5,
                            orig_color[3]
                        )
                
                # Increase roughness for less shiny/cartoony look
                if 'Roughness' in from_node.inputs:
                    current_rough = from_node.inputs['Roughness'].default_value
                    from_node.inputs['Roughness'].default_value = min(0.7, current_rough + 0.3)
                
                # Reduce metallic slightly
                if 'Metallic' in from_node.inputs:
                    current_metal = from_node.inputs['Metallic'].default_value
                    from_node.inputs['Metallic'].default_value = max(0.3, current_metal * 0.7)

# ============================================
# CAMERA - Dramatic angle
# ============================================

print("Setting up camera...")

bpy.ops.object.camera_add(location=(-9, -7, 3))
camera = bpy.context.active_object
camera.name = "Main_Camera"

# Look at ship
direction = ship.location - camera.location
rot_quat = direction.to_track_quat('-Z', 'Y')
camera.rotation_euler = rot_quat.to_euler()

bpy.context.scene.camera = camera
camera.data.lens = 50
camera.data.clip_end = 1000

# Subtle depth of field
camera.data.dof.use_dof = True
camera.data.dof.focus_object = ship
camera.data.dof.aperture_fstop = 8.0  # Subtle DOF

# ============================================
# RENDER SETTINGS - High quality
# ============================================

print("Configuring render...")

scene = bpy.context.scene
scene.render.engine = 'CYCLES'

try:
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.preferences.addons['cycles'].preferences.get_devices()
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        device.use = True
except:
    scene.cycles.device = 'CPU'

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

scene.cycles.samples = 512
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# Color management - contrasty cinematic look
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Very High Contrast'
scene.view_settings.exposure = -0.3  # Slightly darker
scene.view_settings.gamma = 1.0

# Output
scene.render.filepath = r"C:\Users\noahs\Desktop\ai experiments\blender\cinematic_ship_render.png"
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '16'

# ============================================
# RENDER
# ============================================

print("Rendering cinematic shot...")
bpy.ops.render.render(write_still=True)

print(f"\nDone! Render saved to: {scene.render.filepath}")
