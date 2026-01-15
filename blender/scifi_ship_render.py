import bpy
import math
import random

# ============================================
# SETUP - Clear scene
# ============================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Clear orphan data
for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)

print("Importing mesh...")

# ============================================
# IMPORT THE GLB MODEL
# ============================================
bpy.ops.import_scene.gltf(
    filepath=r"C:\Users\noahs\Desktop\ai experiments\blender\Meshy_AI_A_highly_detailed_or_0112213335_generate.glb"
)

# Get the imported object(s)
imported_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
if not imported_objects:
    imported_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

# Join all mesh parts into one
bpy.ops.object.select_all(action='DESELECT')
for obj in imported_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = imported_objects[0]

if len(imported_objects) > 1:
    bpy.ops.object.join()

ship = bpy.context.active_object
ship.name = "Spaceship"

# Center and normalize scale
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
ship.location = (0, 0, 0)

# Get dimensions and scale to reasonable size
max_dim = max(ship.dimensions)
if max_dim > 0:
    scale_factor = 5.0 / max_dim
    ship.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

print(f"Ship dimensions: {ship.dimensions}")

# ============================================
# SHIP MATERIALS - Sci-Fi Look
# ============================================

def create_hull_material():
    """Main hull - dark metallic with blue tint"""
    mat = bpy.data.materials.new(name="SciFi_Hull")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Noise for surface variation
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 50
    noise.inputs['Detail'].default_value = 8
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-400, 0)
    color_ramp.color_ramp.elements[0].color = (0.02, 0.025, 0.035, 1)  # Dark blue-gray
    color_ramp.color_ramp.elements[1].color = (0.06, 0.07, 0.09, 1)   # Lighter blue-gray
    
    # Principled BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Metallic'].default_value = 0.9
    principled.inputs['Roughness'].default_value = 0.35
    principled.inputs['Specular IOR Level'].default_value = 0.8
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_accent_material():
    """Accent panels - lighter metallic"""
    mat = bpy.data.materials.new(name="SciFi_Accent")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = (0.15, 0.17, 0.2, 1)
    principled.inputs['Metallic'].default_value = 0.95
    principled.inputs['Roughness'].default_value = 0.2
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_glow_material():
    """Engine/light glow - cyan emission"""
    mat = bpy.data.materials.new(name="SciFi_Glow")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Mix emission with principled for realism
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, 100)
    emission.inputs['Color'].default_value = (0.2, 0.8, 1, 1)  # Cyan
    emission.inputs['Strength'].default_value = 15
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, -100)
    principled.inputs['Base Color'].default_value = (0.1, 0.5, 0.7, 1)
    principled.inputs['Emission Color'].default_value = (0.2, 0.8, 1, 1)
    principled.inputs['Emission Strength'].default_value = 10
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_window_material():
    """Windows - dark with slight reflection"""
    mat = bpy.data.materials.new(name="SciFi_Windows")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = (0.01, 0.01, 0.02, 1)
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.1
    principled.inputs['Specular IOR Level'].default_value = 1.0
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

print("Applying materials...")

# Clear existing materials and apply new ones
ship.data.materials.clear()
hull_mat = create_hull_material()
ship.data.materials.append(hull_mat)

# ============================================
# SPACE ENVIRONMENT
# ============================================

print("Creating space environment...")

def create_space_world():
    """Deep space background with nebula colors"""
    world = bpy.data.worlds.new(name="Space_World")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()
    
    # Texture coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1200, 0)
    
    # Noise for nebula
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (-900, 200)
    noise1.inputs['Scale'].default_value = 1.5
    noise1.inputs['Detail'].default_value = 6
    
    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (-900, -100)
    noise2.inputs['Scale'].default_value = 3
    noise2.inputs['Detail'].default_value = 8
    
    # Color ramps for nebula colors
    ramp1 = nodes.new('ShaderNodeValToRGB')
    ramp1.location = (-600, 200)
    ramp1.color_ramp.elements[0].position = 0.4
    ramp1.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp1.color_ramp.elements[1].position = 0.7
    ramp1.color_ramp.elements[1].color = (0.05, 0.02, 0.1, 1)  # Purple
    
    ramp2 = nodes.new('ShaderNodeValToRGB')
    ramp2.location = (-600, -100)
    ramp2.color_ramp.elements[0].position = 0.5
    ramp2.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp2.color_ramp.elements[1].position = 0.8
    ramp2.color_ramp.elements[1].color = (0.02, 0.05, 0.12, 1)  # Blue
    
    # Mix nebula colors
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-300, 100)
    mix.blend_type = 'ADD'
    mix.inputs['Fac'].default_value = 1.0
    
    # Stars using voronoi
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-900, -400)
    voronoi.inputs['Scale'].default_value = 500
    voronoi.feature = 'DISTANCE_TO_EDGE'
    
    star_ramp = nodes.new('ShaderNodeValToRGB')
    star_ramp.location = (-600, -400)
    star_ramp.color_ramp.elements[0].position = 0.0
    star_ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    star_ramp.color_ramp.elements[1].position = 0.02
    star_ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    
    # Combine stars and nebula
    mix2 = nodes.new('ShaderNodeMixRGB')
    mix2.location = (-100, 0)
    mix2.blend_type = 'ADD'
    mix2.inputs['Fac'].default_value = 1.0
    
    # Background
    background = nodes.new('ShaderNodeBackground')
    background.location = (100, 0)
    background.inputs['Strength'].default_value = 1.0
    
    output = nodes.new('ShaderNodeOutputWorld')
    output.location = (300, 0)
    
    # Connect everything
    links.new(tex_coord.outputs['Generated'], noise1.inputs['Vector'])
    links.new(tex_coord.outputs['Generated'], noise2.inputs['Vector'])
    links.new(tex_coord.outputs['Generated'], voronoi.inputs['Vector'])
    links.new(noise1.outputs['Fac'], ramp1.inputs['Fac'])
    links.new(noise2.outputs['Fac'], ramp2.inputs['Fac'])
    links.new(ramp1.outputs['Color'], mix.inputs['Color1'])
    links.new(ramp2.outputs['Color'], mix.inputs['Color2'])
    links.new(voronoi.outputs['Distance'], star_ramp.inputs['Fac'])
    links.new(mix.outputs['Color'], mix2.inputs['Color1'])
    links.new(star_ramp.outputs['Color'], mix2.inputs['Color2'])
    links.new(mix2.outputs['Color'], background.inputs['Color'])
    links.new(background.outputs['Background'], output.inputs['Surface'])

create_space_world()

# ============================================
# PLANET
# ============================================

print("Creating planet...")

def create_planet():
    """Rocky/ice planet in background"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=8,
        segments=64,
        ring_count=32,
        location=(25, 30, -5)
    )
    planet = bpy.context.active_object
    planet.name = "Planet"
    
    # Planet material
    mat = bpy.data.materials.new(name="Planet_Surface")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    # Surface noise
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (-600, 100)
    noise1.inputs['Scale'].default_value = 4
    noise1.inputs['Detail'].default_value = 10
    
    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (-600, -100)
    noise2.inputs['Scale'].default_value = 20
    noise2.inputs['Detail'].default_value = 6
    
    # Color ramp - icy blue planet
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-300, 0)
    ramp.color_ramp.elements[0].color = (0.1, 0.15, 0.25, 1)  # Dark blue
    ramp.color_ramp.elements[1].color = (0.4, 0.5, 0.6, 1)    # Light gray-blue
    
    mix_noise = nodes.new('ShaderNodeMixRGB')
    mix_noise.location = (-400, 0)
    mix_noise.inputs['Fac'].default_value = 0.5
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Roughness'].default_value = 0.8
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(tex_coord.outputs['Object'], noise1.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], noise2.inputs['Vector'])
    links.new(noise1.outputs['Fac'], mix_noise.inputs['Color1'])
    links.new(noise2.outputs['Fac'], mix_noise.inputs['Color2'])
    links.new(mix_noise.outputs['Color'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    planet.data.materials.append(mat)
    
    # Atmosphere glow
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=8.3,
        segments=32,
        ring_count=16,
        location=(25, 30, -5)
    )
    atmo = bpy.context.active_object
    atmo.name = "Atmosphere"
    
    atmo_mat = bpy.data.materials.new(name="Atmosphere")
    atmo_mat.use_nodes = True
    atmo_mat.blend_method = 'BLEND'
    nodes = atmo_mat.node_tree.nodes
    links = atmo_mat.node_tree.links
    nodes.clear()
    
    # Fresnel for edge glow
    fresnel = nodes.new('ShaderNodeFresnel')
    fresnel.location = (-300, 0)
    fresnel.inputs['IOR'].default_value = 1.1
    
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, 100)
    emission.inputs['Color'].default_value = (0.3, 0.5, 0.8, 1)
    emission.inputs['Strength'].default_value = 2
    
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    transparent.location = (0, -100)
    
    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (200, 0)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(fresnel.outputs['Fac'], mix.inputs['Fac'])
    links.new(transparent.outputs['BSDF'], mix.inputs[1])
    links.new(emission.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'], output.inputs['Surface'])
    
    atmo.data.materials.append(atmo_mat)
    
    return planet

create_planet()

# ============================================
# LIGHTING
# ============================================

print("Setting up lighting...")

# Key light - main sun/star light
bpy.ops.object.light_add(type='SUN', location=(10, -10, 10))
key_light = bpy.context.active_object
key_light.name = "Key_Sun"
key_light.data.energy = 5
key_light.data.color = (1, 0.95, 0.9)
key_light.data.angle = math.radians(1)
key_light.rotation_euler = (math.radians(45), math.radians(20), math.radians(30))

# Rim light - blue backlight
bpy.ops.object.light_add(type='AREA', location=(-6, 8, 3))
rim_light = bpy.context.active_object
rim_light.name = "Rim_Light"
rim_light.data.energy = 800
rim_light.data.color = (0.4, 0.6, 1)
rim_light.data.size = 4
rim_light.rotation_euler = (math.radians(60), 0, math.radians(-150))

# Fill light - subtle warm
bpy.ops.object.light_add(type='AREA', location=(0, -10, -2))
fill_light = bpy.context.active_object
fill_light.name = "Fill_Light"
fill_light.data.energy = 200
fill_light.data.color = (1, 0.9, 0.8)
fill_light.data.size = 6
fill_light.rotation_euler = (math.radians(100), 0, 0)

# Accent light - engine area
bpy.ops.object.light_add(type='SPOT', location=(-5, 0, 0))
accent_light = bpy.context.active_object
accent_light.name = "Engine_Accent"
accent_light.data.energy = 500
accent_light.data.color = (0.3, 0.8, 1)
accent_light.data.spot_size = math.radians(60)
accent_light.data.spot_blend = 0.5
accent_light.rotation_euler = (math.radians(90), 0, math.radians(90))

# ============================================
# CAMERA
# ============================================

print("Setting up camera...")

bpy.ops.object.camera_add(location=(-10, -8, 4))
camera = bpy.context.active_object
camera.name = "Main_Camera"

# Point at ship
direction = ship.location - camera.location
rot_quat = direction.to_track_quat('-Z', 'Y')
camera.rotation_euler = rot_quat.to_euler()

# Adjust for better composition
camera.rotation_euler.x += math.radians(5)
camera.rotation_euler.z += math.radians(-5)

bpy.context.scene.camera = camera

# Camera settings
camera.data.lens = 50
camera.data.dof.use_dof = True
camera.data.dof.focus_object = ship
camera.data.dof.aperture_fstop = 4.0
camera.data.clip_end = 1000

# ============================================
# RENDER SETTINGS
# ============================================

print("Configuring render...")

scene = bpy.context.scene

# Cycles for quality
scene.render.engine = 'CYCLES'

# Try GPU
try:
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.preferences.addons['cycles'].preferences.get_devices()
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        device.use = True
except:
    scene.cycles.device = 'CPU'

# High quality settings
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

scene.cycles.samples = 512
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# Film settings
scene.render.film_transparent = False
scene.view_settings.look = 'AgX - Medium High Contrast'

# Output
scene.render.filepath = r"C:\Users\noahs\Desktop\ai experiments\blender\scifi_ship_render.png"
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '16'

# ============================================
# RENDER
# ============================================

print("Rendering... this may take a few minutes...")
bpy.ops.render.render(write_still=True)

print(f"\nDone! Render saved to: {scene.render.filepath}")
