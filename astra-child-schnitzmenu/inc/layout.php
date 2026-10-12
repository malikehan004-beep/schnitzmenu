<?php
/**
 * Site-wide layout pieces hooked into Astra: sidebar box, footer disclaimer,
 * floating meal builder and back-to-top button.
 *
 * @package schnitzmenu
 */

defined( 'ABSPATH' ) || exit;

/**
 * Sidebar box shown under any widgets (AdSense goes in the widgets above it).
 */
function sm_sidebar_box() {
	if ( ! get_option( 'sm_sidebar_box', 1 ) ) {
		return;
	}
	echo '<div class="sm-sidebar">';
	echo do_shortcode( '[sm_updated]' );
	echo '<h3 class="sm-sidebar__title">Schnitz guides</h3><ul class="sm-sidebar__links">';
	foreach ( sm_site_pages() as $slug => $page ) {
		echo '<li><a href="' . esc_url( home_url( '/' . $slug . '/' ) ) . '">' . sm_icon( $page[2] ) . esc_html( $page[0] ) . '</a></li>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- icon is static SVG.
	}
	echo '</ul>';
	echo sm_order_buttons(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped inside.
	echo '</div>';
}
add_action( 'astra_sidebars_after', 'sm_sidebar_box' );

/**
 * Disclaimer strip above the footer on every page (AdSense + legal requirement).
 */
function sm_footer_disclaimer() {
	echo '<div class="sm-footer-disclaimer"><div class="ast-container">';
	echo sm_disclaimer_html(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static HTML.
	if ( has_nav_menu( 'sm_footer' ) ) {
		wp_nav_menu( array(
			'theme_location' => 'sm_footer',
			'container'      => 'nav',
			'container_class'=> 'sm-footer-links',
			'depth'          => 1,
			'fallback_cb'    => false,
		) );
	}
	echo '</div></div>';
}
add_action( 'astra_footer_before', 'sm_footer_disclaimer' );

/**
 * Floating meal builder (stays hidden until someone presses a "+" button) and back-to-top.
 */
function sm_footer_widgets() {
	if ( is_singular() ) {
		echo do_shortcode( '[sm_meal_builder]' );
	}
	echo '<a href="#" class="sm-top" aria-label="Back to top" hidden>&uarr;</a>';
}
add_action( 'wp_footer', 'sm_footer_widgets' );
