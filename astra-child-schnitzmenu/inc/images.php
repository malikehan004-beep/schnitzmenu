<?php
/**
 * Images: responsive <img> output, category grid, social share (Open Graph) images,
 * favicon fallback, LCP preload and a one-click "copy to Media Library" tool.
 *
 * All images are original illustrations bundled in assets/img/ (WebP, 3-21 KB each).
 *
 * @package schnitzmenu
 */

defined( 'ABSPATH' ) || exit;

/**
 * Bundled illustrations: name => [widths, intrinsic width, intrinsic height, default alt].
 *
 * @return array
 */
function sm_images() {
	return array(
		'hero-schnitzel-plate' => array( array( 520, 1000 ), 1000, 800, 'Illustration of a crumbed schnitzel with chips, slaw, lemon and dip - Schnitz menu Australia' ),
		'cat-plates'           => array( array( 400, 800 ), 800, 500, 'Schnitz parma and chips plate illustration' ),
		'cat-wraps-burgers'    => array( array( 400, 800 ), 800, 500, 'Schnitz schnitzel burger and wrap illustration' ),
		'cat-tenders-schnacks' => array( array( 400, 800 ), 800, 500, 'Schnitz chicken tenders with dipping sauces illustration' ),
		'cat-salads'           => array( array( 400, 800 ), 800, 500, 'Schnitz salad with schnitzel strips illustration' ),
		'cat-kids'             => array( array( 400, 800 ), 800, 500, 'Schnitz kids meal box with schnuggets, chips and a drink illustration' ),
		'cat-chips-dips'       => array( array( 400, 800 ), 800, 500, 'Schnitz chips and dipping sauces illustration' ),
		'cat-drinks'           => array( array( 400, 800 ), 800, 500, 'Soft drink cans and bottled water illustration' ),
	);
}

/**
 * Responsive image tag with srcset, explicit size (no layout shift) and lazy loading.
 *
 * @param string $name  Image key from sm_images().
 * @param array  $args  alt, sizes, class, eager (bool).
 * @return string
 */
function sm_image_html( $name, $args = array() ) {
	$images = sm_images();
	if ( ! isset( $images[ $name ] ) ) {
		return '';
	}
	list( $widths, $w, $h, $alt ) = $images[ $name ];
	$args = wp_parse_args( $args, array(
		'alt'   => $alt,
		'sizes' => '(max-width: 767px) 100vw, 400px',
		'class' => '',
		'eager' => false,
	) );

	$srcset = array();
	foreach ( $widths as $width ) {
		$srcset[] = esc_url( SM_URI . "/assets/img/{$name}-{$width}.webp" ) . " {$width}w";
	}
	$src = SM_URI . "/assets/img/{$name}-" . end( $widths ) . '.webp';

	$attrs = $args['eager']
		? ' loading="eager" fetchpriority="high" decoding="async"'
		: ' loading="lazy" decoding="async"';

	return '<img class="sm-img ' . esc_attr( $args['class'] ) . '" src="' . esc_url( $src ) . '" srcset="' . implode( ', ', $srcset ) . '"'
		. ' sizes="' . esc_attr( $args['sizes'] ) . '" width="' . (int) $w . '" height="' . (int) $h . '"'
		. ' alt="' . esc_attr( $args['alt'] ) . '"' . $attrs . '>';
}

add_shortcode( 'sm_image', function ( $atts ) {
	$atts = shortcode_atts( array(
		'name'  => 'hero-schnitzel-plate',
		'alt'   => '',
		'sizes' => '',
		'class' => '',
		'eager' => 'no',
	), $atts );
	$args = array(
		'class' => $atts['class'],
		'eager' => 'yes' === $atts['eager'],
	);
	if ( $atts['alt'] ) {
		$args['alt'] = $atts['alt'];
	}
	if ( $atts['sizes'] ) {
		$args['sizes'] = $atts['sizes'];
	}
	return sm_image_html( $atts['name'], $args );
} );

/**
 * Category image for a menu category slug (falls back to the plates image).
 *
 * @param string $slug Category slug.
 * @return string Image key.
 */
function sm_category_image( $slug ) {
	$key = 'cat-' . $slug;
	return isset( sm_images()[ $key ] ) ? $key : 'cat-plates';
}

/**
 * [sm_category_grid] - picture cards linking to each category on the menu page.
 */
add_shortcode( 'sm_category_grid', function () {
	$out = '<div class="sm-cat-grid">';
	foreach ( sm_categories() as $cat ) {
		$prices = array_filter( wp_list_pluck( $cat['items'], 'price' ), 'is_numeric' );
		$from   = $prices ? 'From $' . number_format( min( $prices ), 2 ) . ' (approx.)' : count( $cat['items'] ) . ' items';
		$out   .= '<a class="sm-cat-card" href="' . esc_url( home_url( '/schnitz-menu/#sm-cat-' . $cat['slug'] ) ) . '">'
			. sm_image_html( sm_category_image( $cat['slug'] ), array(
				'alt'   => 'Schnitz ' . $cat['name'] . ' menu',
				'sizes' => '(max-width: 600px) 50vw, (max-width: 1100px) 33vw, 290px',
			) )
			. '<span class="sm-cat-card__body"><strong>' . esc_html( $cat['name'] ) . '</strong><span>' . esc_html( $from ) . '</span></span></a>';
	}
	return $out . '</div>';
} );

/* ---------------------------------------------------------------------------
 * Social share images (Open Graph / Twitter)
 * ------------------------------------------------------------------------- */

/**
 * Share image URL for the current page.
 *
 * @return string
 */
function sm_og_image_url() {
	$slug = 'home';
	if ( is_singular() && ! is_front_page() ) {
		$slug = get_post_field( 'post_name', get_queried_object_id() );
	}
	$file = '/assets/img/og/og-' . sanitize_file_name( $slug ) . '.jpg';
	if ( ! file_exists( SM_DIR . $file ) ) {
		$file = '/assets/img/og/og-home.jpg';
	}
	return SM_URI . $file;
}

/**
 * Rank Math: use our card when no image has been chosen for the page.
 *
 * @param string $image Image URL chosen by Rank Math.
 * @return string
 */
function sm_rank_math_og_image( $image ) {
	return $image ? $image : sm_og_image_url();
}
add_filter( 'rank_math/opengraph/facebook/image', 'sm_rank_math_og_image' );
add_filter( 'rank_math/opengraph/twitter/image', 'sm_rank_math_og_image' );

/**
 * Without an SEO plugin, print basic share tags ourselves.
 */
function sm_fallback_social_tags() {
	if ( defined( 'RANK_MATH_VERSION' ) || defined( 'WPSEO_VERSION' ) ) {
		return;
	}
	$url = sm_og_image_url();
	echo '<meta property="og:image" content="' . esc_url( $url ) . '">' . "\n";
	echo '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">' . "\n";
	echo '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="' . esc_url( $url ) . '">' . "\n";
}
add_action( 'wp_head', 'sm_fallback_social_tags', 5 );

/**
 * Favicon + home-screen icon until a Site Icon is set in the Customizer.
 */
function sm_fallback_icons() {
	if ( has_site_icon() ) {
		return;
	}
	echo '<link rel="icon" href="' . esc_url( SM_URI . '/assets/img/favicon.ico' ) . '" sizes="any">' . "\n";
	echo '<link rel="icon" type="image/png" href="' . esc_url( SM_URI . '/assets/img/site-icon-512.png' ) . '">' . "\n";
	echo '<link rel="apple-touch-icon" href="' . esc_url( SM_URI . '/assets/img/apple-touch-icon.png' ) . '">' . "\n";
	echo '<meta name="theme-color" content="#C74214">' . "\n";
}
add_action( 'wp_head', 'sm_fallback_icons', 6 );

/**
 * Preload the hero illustration on the home page (it's the Largest Contentful Paint).
 */
function sm_preload_hero() {
	if ( ! is_front_page() ) {
		return;
	}
	printf(
		'<link rel="preload" as="image" type="image/webp" href="%1$s" imagesrcset="%2$s 520w, %1$s 1000w" imagesizes="(max-width: 767px) 92vw, 460px" fetchpriority="high">' . "\n",
		esc_url( SM_URI . '/assets/img/hero-schnitzel-plate-1000.webp' ),
		esc_url( SM_URI . '/assets/img/hero-schnitzel-plate-520.webp' )
	);
}
add_action( 'wp_head', 'sm_preload_hero', 2 );

/* ---------------------------------------------------------------------------
 * Copy the illustrations into the Media Library (so they can be used in any
 * Elementor Image widget, with alt text already filled in).
 * ------------------------------------------------------------------------- */

/**
 * Handle the admin-post action.
 */
function sm_import_media() {
	if ( ! current_user_can( 'upload_files' ) ) {
		wp_die( esc_html__( 'You are not allowed to upload files.', 'schnitzmenu' ) );
	}
	check_admin_referer( 'sm_import_media' );
	require_once ABSPATH . 'wp-admin/includes/image.php';

	$added = 0;
	foreach ( sm_images() as $name => $info ) {
		$file = SM_DIR . "/assets/img/{$name}-" . end( $info[0] ) . '.webp';
		$existing = get_posts( array(
			'post_type'   => 'attachment',
			'post_status' => 'inherit',
			'meta_key'    => '_sm_asset', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key
			'meta_value'  => $name, // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_value
			'fields'      => 'ids',
		) );
		if ( $existing || ! is_readable( $file ) ) {
			continue;
		}
		$upload = wp_upload_bits( "schnitzmenu-{$name}.webp", null, file_get_contents( $file ) ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
		if ( ! empty( $upload['error'] ) ) {
			continue;
		}
		$id = wp_insert_attachment( array(
			'post_title'     => ucwords( str_replace( '-', ' ', $name ) ),
			'post_mime_type' => 'image/webp',
			'post_status'    => 'inherit',
		), $upload['file'] );
		if ( is_wp_error( $id ) ) {
			continue;
		}
		wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $upload['file'] ) );
		update_post_meta( $id, '_wp_attachment_image_alt', $info[3] );
		update_post_meta( $id, '_sm_asset', $name );
		++$added;
	}
	wp_safe_redirect( add_query_arg( 'sm_media_added', $added, admin_url( 'themes.php?page=sm-data' ) ) );
	exit;
}
add_action( 'admin_post_sm_import_media', 'sm_import_media' );
