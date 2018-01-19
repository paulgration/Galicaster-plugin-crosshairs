from galicaster.core import context

import cairo
import gi
gi.require_foreign('cairo')

# Galicaster constants
conf = context.get_conf()
dispatcher = context.get_dispatcher()
logger = context.get_logger()

def init():
    Crosshairs()

class Crosshairs(object):
    def __init__(self):
        # Persistent ImageSurface on to which the crosshair will be drawn
        self.p_image_surface = None
        # Pipeline is ready (triggers with each pipeline change)
        dispatcher.connect('recorder-ready', self.on_recorder_ready)

    def on_recorder_ready(self, _source):
        # Reset image_surface so crosshair is redrawn each time the pipeline is changed
        self.p_image_surface = None

        recorder = context.get_recorder().recorder
        for recorder_bin in recorder.bins.values():
            # Check for specific flavor
            if recorder_bin.get_bins_info()[0].get('flavor') == 'presenter':
                # Get overlay element
                overlay = recorder_bin.get_by_name('crosshair-overlay')
                if overlay:
                    overlay.connect('draw', self.on_draw)

    def on_draw(self, _overlay, ctx, _timestamp, _duration):
        if not self.p_image_surface:
            # Image surface for the cairo overlay element
            image_surface = ctx.get_target()

            # Drawable surface (video) dimensions
            surface_w = image_surface.get_width()
            surface_h = image_surface.get_height()

            # New persistent ImageSurface to draw the crosshair once
            self.p_image_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, surface_w, surface_h)

            # Persistent ImageSurface context
            p_ctx = cairo.Context(self.p_image_surface)

            # Surface halves (for centering)
            surface_w_half = surface_w / 2
            surface_h_half = surface_h / 2

            # Hair thickness and length (these seem to be reasonable sizes)
            hair_t = surface_w / 128
            hair_l = surface_h / 2

            # Hair halves (for centering)
            hair_t_half = hair_t / 2
            hair_l_half = hair_l / 2

            # Outer faces of crosshair
            outer_l = surface_w_half - hair_l_half
            outer_t = surface_h_half - hair_l_half
            outer_r = surface_w_half + hair_l_half
            outer_b = surface_h_half + hair_l_half

            # Inner faces of crosshair
            inner_l = surface_w_half - hair_t_half
            inner_t = surface_h_half - hair_t_half
            inner_r = surface_w_half + hair_t_half
            inner_b = surface_h_half + hair_t_half

            # Draw crosshair
            p_ctx.move_to(outer_l, inner_t)
            p_ctx.line_to(inner_l, inner_t)
            p_ctx.line_to(inner_l, outer_t)
            p_ctx.line_to(inner_r, outer_t)
            p_ctx.line_to(inner_r, inner_t)
            p_ctx.line_to(outer_r, inner_t)
            p_ctx.line_to(outer_r, inner_b)
            p_ctx.line_to(inner_r, inner_b)
            p_ctx.line_to(inner_r, inner_b)
            p_ctx.line_to(inner_r, outer_b)
            p_ctx.line_to(inner_l, outer_b)
            p_ctx.line_to(inner_l, inner_b)
            p_ctx.line_to(outer_l, inner_b)
            p_ctx.close_path()
            p_ctx.set_source_rgb(1, 1, 1)
            p_ctx.fill_preserve()
            p_ctx.set_source_rgb(0, 0, 0)
            p_ctx.stroke()
        else:
            # Paint stored crosshair rather than recalculate/redraw on each frame
            ctx.set_source_surface(self.p_image_surface)
            ctx.paint()
