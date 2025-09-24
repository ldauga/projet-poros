from minescript import (
    java_class, java_member, java_access_field, java_call_method,
    java_float, java_release, version_info, echo
)

# 0) (optional) sanity: confirm we’re on 1.21.4 and client is visible
info = version_info()
echo(f"MC={info.minecraft} main={info.minecraft_class_name}")

# 1) MinecraftClient.getInstance()
mc_cls = java_class("net.minecraft.class_310")
m_getInstance = java_member(mc_cls, "method_1551")  # static getter
mc = java_call_method(mc_cls, m_getInstance)        # call static on class handle

# 2) SoundManager from the client
f_soundManager = java_member(mc_cls, "field_1730")
sm = java_access_field(mc, f_soundManager)

# 3) Build a PositionedSoundInstance via master(SoundEvent, float)
psi_cls = java_class("net.minecraft.class_1147")
m_master = java_member(psi_cls, "method_4898")      # static factory
se = sound_const("minecraft:block.note_block.harp") # or any namespaced sound id
vol = java_float(volume if 'volume' in globals() else 1.0)

snd = java_call_method(psi_cls, m_master, se, vol)  # static call -> SoundInstance

# 4) SoundManager.play(SoundInstance)
sm_cls = java_class("net.minecraft.class_1144")
m_play = java_member(sm_cls, "method_4892")
java_call_method(sm, m_play, snd)

# (optional) clean up Java refs if you won’t reuse them
java_release(snd, se, vol, m_play, sm_cls, m_master, psi_cls, sm, f_soundManager, mc, m_getInstance,