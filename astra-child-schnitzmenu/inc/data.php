<?php
/**
 * Menu data: loads the bundled data/menu.json, or the copy saved in
 * Appearance > Schnitz Menu Data (which wins once saved).
 *
 * @package schnitzmenu
 */

defined( 'ABSPATH' ) || exit;

/**
 * All menu data as an array.
 *
 * @return array
 */
function sm_data() {
	static $data = null;
	if ( null !== $data ) {
		return $data;
	}

	$data = array();
	$json = get_option( 'sm_menu_json', '' );
	if ( $json ) {
		$decoded = json_decode( $json, true );
		if ( is_array( $decoded ) ) {
			$data = $decoded;
		}
	}
	if ( ! $data ) {
		$data = sm_default_data();
	}
	return $data;
}

/**
 * The bundled data file.
 *
 * @return array
 */
function sm_default_data() {
	$file = SM_DIR . '/data/menu.json';
	if ( ! is_readable( $file ) ) {
		return array();
	}
	$decoded = json_decode( (string) file_get_contents( $file ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
	return is_array( $decoded ) ? $decoded : array();
}

/**
 * "October 2026" style label for the last data refresh.
 *
 * @return string
 */
function sm_updated_label() {
	$label = get_option( 'sm_updated', '' );
	if ( ! $label ) {
		$data  = sm_data();
		$label = isset( $data['updated'] ) ? $data['updated'] : '';
	}
	return $label ? $label : wp_date( 'F Y' );
}

/**
 * Categories, optionally filtered by a comma separated list of slugs.
 *
 * @param string $slugs Comma separated slugs, or empty for all.
 * @return array
 */
function sm_categories( $slugs = '' ) {
	$data = sm_data();
	$cats = isset( $data['categories'] ) ? $data['categories'] : array();
	if ( '' === trim( $slugs ) ) {
		return $cats;
	}
	$wanted = array_map( 'trim', explode( ',', $slugs ) );
	$out    = array();
	foreach ( $wanted as $slug ) {
		foreach ( $cats as $cat ) {
			if ( $cat['slug'] === $slug ) {
				$out[] = $cat;
			}
		}
	}
	return $out;
}

/**
 * Every item across all categories, with its category name attached.
 *
 * @return array
 */
function sm_all_items() {
	$items = array();
	foreach ( sm_categories() as $cat ) {
		foreach ( $cat['items'] as $item ) {
			$item['category'] = $cat['name'];
			$items[]          = $item;
		}
	}
	return $items;
}

/**
 * Price as "$19.50 (approx.)", or "Varies" when we haven't verified one.
 *
 * @param float|null $price Price in AUD.
 * @return string HTML.
 */
function sm_price_html( $price ) {
	if ( null === $price || '' === $price ) {
		return '<span class="sm-muted">Varies</span>';
	}
	return '$' . esc_html( number_format( (float) $price, 2 ) ) . ' <span class="sm-approx">(approx.)</span>';
}

/**
 * Calories as "779 kcal", or a dash when unknown.
 *
 * @param int|null $kcal Calories.
 * @return string HTML.
 */
function sm_kcal_html( $kcal ) {
	if ( null === $kcal || '' === $kcal ) {
		return '<span class="sm-muted">&mdash;</span>';
	}
	return esc_html( number_format( (int) $kcal ) ) . ' kcal';
}
