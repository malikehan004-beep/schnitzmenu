<?php
/**
 * SchnitzMenu - Astra child theme.
 *
 * @package schnitzmenu
 */

defined( 'ABSPATH' ) || exit;

define( 'SM_VERSION', '1.0.0' );
define( 'SM_DIR', get_stylesheet_directory() );
define( 'SM_URI', get_stylesheet_directory_uri() );

require_once SM_DIR . '/inc/data.php';
require_once SM_DIR . '/inc/shortcodes.php';
require_once SM_DIR . '/inc/layout.php';
require_once SM_DIR . '/inc/admin.php';

/**
 * Styles and scripts.
 */
function sm_enqueue_assets() {
	wp_enqueue_style(
		'sm-fonts',
		'https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Open+Sans:wght@400;600&display=swap',
		array(),
		null
	);
	wp_enqueue_style( 'sm-child', SM_URI . '/assets/css/schnitz.css', array( 'astra-theme-css' ), SM_VERSION );
	wp_enqueue_script( 'sm-child', SM_URI . '/assets/js/schnitz.js', array(), SM_VERSION, true );
	wp_script_add_data( 'sm-child', 'strategy', 'defer' );
}
add_action( 'wp_enqueue_scripts', 'sm_enqueue_assets', 20 );

/**
 * Preconnect to Google Fonts so the fonts don't delay first paint.
 *
 * @param array  $urls          URLs to print for resource hints.
 * @param string $relation_type The relation type the URLs are printed for.
 * @return array
 */
function sm_resource_hints( $urls, $relation_type ) {
	if ( 'preconnect' === $relation_type ) {
		$urls[] = 'https://fonts.googleapis.com';
		$urls[] = array(
			'href'        => 'https://fonts.gstatic.com',
			'crossorigin' => 'anonymous',
		);
	}
	return $urls;
}
add_filter( 'wp_resource_hints', 'sm_resource_hints', 10, 2 );

/**
 * Theme supports and menus.
 */
function sm_setup() {
	add_theme_support( 'custom-logo', array(
		'height'      => 60,
		'width'       => 240,
		'flex-width'  => true,
		'flex-height' => true,
	) );
	register_nav_menu( 'sm_footer', __( 'Footer Legal Links', 'schnitzmenu' ) );
}
add_action( 'after_setup_theme', 'sm_setup', 20 );

/**
 * On activation, stop Elementor's stock colours/fonts (blue headings, Roboto) overriding the theme.
 * Same as ticking Elementor > Settings > "Disable Default Colors" and "Disable Default Fonts".
 */
function sm_on_activate() {
	update_option( 'elementor_disable_color_schemes', 'yes' );
	update_option( 'elementor_disable_typography_schemes', 'yes' );
}
add_action( 'after_switch_theme', 'sm_on_activate' );

/**
 * Astra defaults that match the blueprint (only used until you change them in the Customizer).
 *
 * @param array $defaults Astra default options.
 * @return array
 */
function sm_astra_defaults( $defaults ) {
	$defaults['site-content-width']   = 1200;
	$defaults['site-sidebar-layout']  = 'right-sidebar';
	$defaults['body-font-family']     = "'Open Sans', sans-serif";
	$defaults['headings-font-family'] = "'Montserrat', sans-serif";
	$defaults['headings-font-weight'] = '700';
	return $defaults;
}
add_filter( 'astra_theme_defaults', 'sm_astra_defaults' );
