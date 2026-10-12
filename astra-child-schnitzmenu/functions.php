<?php
/**
 * SchnitzMenu - Astra child theme.
 *
 * @package schnitzmenu
 */

defined( 'ABSPATH' ) || exit;

define( 'SM_VERSION', '1.1.0' );
define( 'SM_DIR', get_stylesheet_directory() );
define( 'SM_URI', get_stylesheet_directory_uri() );

require_once SM_DIR . '/inc/data.php';
require_once SM_DIR . '/inc/shortcodes.php';
require_once SM_DIR . '/inc/layout.php';
require_once SM_DIR . '/inc/admin.php';
require_once SM_DIR . '/inc/images.php';
require_once SM_DIR . '/inc/performance.php';

/**
 * Styles and scripts. Fonts are self-hosted (see assets/css/schnitz.css), so there is
 * no request to Google Fonts.
 */
function sm_enqueue_assets() {
	wp_enqueue_style( 'sm-child', SM_URI . '/' . sm_asset( 'assets/css/schnitz.css' ), array( 'astra-theme-css' ), SM_VERSION );
	wp_enqueue_script( 'sm-child', SM_URI . '/' . sm_asset( 'assets/js/schnitz.js' ), array(), SM_VERSION, true );
	wp_script_add_data( 'sm-child', 'strategy', 'defer' );
}
add_action( 'wp_enqueue_scripts', 'sm_enqueue_assets', 20 );

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
