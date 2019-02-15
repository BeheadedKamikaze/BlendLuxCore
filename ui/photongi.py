from bl_ui.properties_render import RenderButtonsPanel
from bpy.types import Panel
from . import icons


class LUXCORE_RENDER_PT_photongi(RenderButtonsPanel, Panel):
    COMPAT_ENGINES = {"LUXCORE"}
    bl_label = "LuxCore PhotonGI Cache"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "LUXCORE"

    def draw_header(self, context):
        self.layout.prop(context.scene.luxcore.config.photongi, "enabled", text="")

    def draw(self, context):
        layout = self.layout
        photongi = context.scene.luxcore.config.photongi
        layout.active = photongi.enabled

        if context.scene.luxcore.config.engine == "BIDIR":
            layout.label(text="Not supported by Bidir", icon=icons.INFO)

        if not photongi.indirect_enabled and not photongi.caustic_enabled:
            layout.label(text="All caches disabled", icon=icons.WARNING)

        row = layout.row(align=True)
        row.prop(photongi, "photon_maxcount")
        row.prop(photongi, "photon_maxdepth")

        col = layout.column(align=True)
        col.prop(photongi, "indirect_enabled")
        col = col.column(align=True)
        col.active = photongi.indirect_enabled
        col.prop(photongi, "indirect_maxsize")
        col.prop(photongi, "indirect_lookup_radius")
        col.prop(photongi, "indirect_usagethresholdscale")
        col.prop(photongi, "indirect_glossinessusagethreshold")

        col = layout.column(align=True)
        col.prop(photongi, "caustic_enabled")
        row = col.row(align=True)
        row.active = photongi.caustic_enabled
        row.prop(photongi, "caustic_maxsize")
        row = col.row(align=True)
        row.active = photongi.caustic_enabled
        row.prop(photongi, "caustic_lookup_radius")
        row.prop(photongi, "caustic_lookup_maxcount")

        layout.prop(photongi, "debug")
        if (photongi.debug == "showindirect" and not photongi.indirect_enabled) or (
                photongi.debug == "showcaustic" and not photongi.caustic_enabled):
            layout.label(text="Can't show this cache (disabled)", icon=icons.WARNING)