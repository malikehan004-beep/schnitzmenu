<?php
/**
 * Speed: self-hosted fonts, no third-party font requests, no emoji script.
 *
 * @package schnitzmenu
 */

defined( 'ABSPATH' ) || exit;

/**
 * Preload the two fonts every page uses first (headings + body text).
 */
function sm_preload_fonts() {
	foreach ( array( 'montserrat-latin-700-normal.woff2', 'open-sans-latin-400-normal.woff2' ) as $font ) {
		echo '<link rel="preload" href="' . esc_url( SM_URI . '/assets/fonts/' . $font ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	}
}
add_action( 'wp_head', 'sm_preload_fonts', 1 );

/*
 * Fonts are bundled with the theme (assets/fonts), so stop Astra and Elementor
 * requesting the same fonts from Google: two fewer connections and no
 * render-blocking CSS from fonts.googleapis.com.
 */
add_filter( 'elementor/frontend/print_google_fonts', '__return_false' );
add_filter( 'astra_google_fonts_selected', function ( $fonts ) {
	unset( $fonts['Montserrat'], $fonts['Open Sans'] );
	return $fonts;
} );

/**
 * Remove WordPress' emoji detection script and styles (~15 KB on every page).
 */
function sm_disable_emojis() {
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
	remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
	remove_action( 'admin_print_styles', 'print_emoji_styles' );
	remove_filter( 'the_content_feed', 'wp_staticize_emoji' );
	remove_filter( 'comment_text_rss', 'wp_staticize_emoji' );
	remove_filter( 'wp_mail', 'wp_staticize_emoji_for_email' );
	add_filter( 'emoji_svg_url', '__return_false' );
}
add_action( 'init', 'sm_disable_emojis' );

/**
 * Minified asset when available (built by tools/minify.js), unless SCRIPT_DEBUG is on.
 *
 * @param string $path Path relative to the theme, e.g. assets/css/schnitz.css.
 * @return string Relative path to use.
 */
function sm_asset( $path ) {
	if ( defined( 'SCRIPT_DEBUG' ) && SCRIPT_DEBUG ) {
		return $path;
	}
	$min = preg_replace( '/\.(css|js)$/', '.min.$1', $path );
	return file_exists( SM_DIR . '/' . $min ) ? $min : $path;
}

/**
 * Move jQuery (and jQuery Migrate) to the footer on the front end so it no longer
 * blocks the first paint. Elementor's own front-end scripts already load in the
 * footer after it. Skipped in the Elementor editor/preview and in wp-admin.
 * Turn off with: add_filter( 'sm_jquery_in_footer', '__return_false' );
 */
function sm_jquery_to_footer() {
	if ( is_admin() || ! apply_filters( 'sm_jquery_in_footer', true ) ) {
		return;
	}
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- read-only check of Elementor's preview flag.
	if ( isset( $_GET['elementor-preview'] ) || ( class_exists( '\Elementor\Plugin' ) && \Elementor\Plugin::$instance->preview && \Elementor\Plugin::$instance->preview->is_preview_mode() ) ) {
		return;
	}
	foreach ( array( 'jquery', 'jquery-core', 'jquery-migrate' ) as $handle ) {
		wp_scripts()->add_data( $handle, 'group', 1 );
	}
}
add_action( 'wp_enqueue_scripts', 'sm_jquery_to_footer', 1 );

/**
 * Meta description from the imported page data when no SEO plugin is active
 * (Rank Math prints its own once installed).
 */
function sm_fallback_meta_description() {
	if ( defined( 'RANK_MATH_VERSION' ) || defined( 'WPSEO_VERSION' ) || ! is_singular() ) {
		return;
	}
	$desc = get_post_meta( get_queried_object_id(), 'rank_math_description', true );
	if ( $desc ) {
		echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
	}
}
add_action( 'wp_head', 'sm_fallback_meta_description', 3 );
