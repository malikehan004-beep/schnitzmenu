<?php
/**
 * Shortcodes. Drop any of these into an Elementor "Shortcode" widget.
 *
 *   [sm_updated]                          "Updated October 2026" badge
 *   [sm_jump_nav]                         sticky jump links to each menu category
 *   [sm_menu_search]                      live search box that filters every table on the page
 *   [sm_price_table cat='plates']         price table for one or more categories
 *   [sm_meal_builder]                     add items, see total price + calories
 *   [sm_calorie_chart top='10']           bar chart of the highest calorie items
 *   [sm_nutrition_table]                  every item with known calories
 *   [sm_allergens]                        allergen matrix by crumb / coating
 *   [sm_faq set='main']                   FAQ accordion + FAQPage schema
 *   [sm_deals]                            deals and bundles table
 *   [sm_order]                            order / find a store buttons
 *   [sm_related pages='a,b,c']            related page cards (internal links)
 *   [sm_menu_schema]                      Menu JSON-LD for Google
 *   [sm_print]                            "Print this menu" button
 *   [sm_disclaimer]                       unofficial-site disclaimer
 *
 * @package schnitzmenu
 */

defined( 'ABSPATH' ) || exit;

/**
 * Pages on the site, used by related links, the sidebar and home cards.
 *
 * @return array slug => [title, description, icon]
 */
function sm_site_pages() {
	return apply_filters( 'sm_site_pages', array(
		'schnitz-menu'           => array( 'Full Schnitz Menu', 'Every item on the menu in one place.', 'menu' ),
		'schnitz-menu-prices'    => array( 'Schnitz Prices 2026', 'Current prices for every wrap, plate and side.', 'tag' ),
		'schnitz-calories'       => array( 'Calories & Nutrition', 'Calorie counts and a top-10 chart.', 'apple' ),
		'schnitz-allergen-menu'  => array( 'Allergen Guide', 'Gluten, egg, milk, soy and sesame by crumb.', 'alert' ),
		'schnitz-kids-menu'      => array( 'Kids Menu', 'Little Rascals meals and prices.', 'star' ),
		'schnitz-coupons'        => array( 'Deals & Coupons', 'Family bundles and value deals.', 'gift' ),
	) );
}

/**
 * Small inline SVG icons (no icon font = faster pages).
 *
 * @param string $name Icon name.
 * @return string
 */
function sm_icon( $name ) {
	$paths = array(
		'menu'  => '<path d="M4 4h16v16H4z"/><path d="M8 8h8M8 12h8M8 16h5"/>',
		'tag'   => '<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
		'apple' => '<path d="M12 7c-2-2-7-1.5-7 4 0 4 3 9 5 9 1 0 1.5-.5 2-.5s1 .5 2 .5c2 0 5-5 5-9 0-5.5-5-6-7-4z"/><path d="M12 7c0-2 1-4 3-4"/>',
		'alert' => '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/>',
		'star'  => '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
		'gift'  => '<path d="M3 9h18v4H3zM5 13h14v8H5zM12 9v12"/><path d="M12 9c-2 0-4-1-4-3s3-2 4 3c1-5 4-5 4-3s-2 3-4 3z"/>',
		'pin'   => '<path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
		'bag'   => '<path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
		'print' => '<path d="M6 9V3h12v6M6 18H4v-7h16v7h-2"/><path d="M6 14h12v7H6z"/>',
		'clock' => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
	);
	$path = isset( $paths[ $name ] ) ? $paths[ $name ] : $paths['menu'];
	return '<svg class="sm-icon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $path . '</svg>';
}

/* ---------------------------------------------------------------------------
 * Badges, navigation, search
 * ------------------------------------------------------------------------- */

add_shortcode( 'sm_updated', function () {
	return '<span class="sm-updated">' . sm_icon( 'clock' ) . ' Updated ' . esc_html( sm_updated_label() ) . '</span>';
} );

add_shortcode( 'sm_jump_nav', function ( $atts ) {
	$atts  = shortcode_atts( array( 'items' => '' ), $atts );
	$links = array();
	if ( $atts['items'] ) {
		// items='id:Label|id:Label'.
		foreach ( explode( '|', $atts['items'] ) as $pair ) {
			$parts = array_map( 'trim', explode( ':', $pair, 2 ) );
			if ( 2 === count( $parts ) ) {
				$links[ $parts[0] ] = $parts[1];
			}
		}
	} else {
		foreach ( sm_categories() as $cat ) {
			$links[ 'sm-cat-' . $cat['slug'] ] = $cat['name'];
		}
	}
	$out = '<nav class="sm-jump" aria-label="Jump to menu section"><ul>';
	foreach ( $links as $id => $label ) {
		$out .= '<li><a href="#' . esc_attr( $id ) . '">' . esc_html( $label ) . '</a></li>';
	}
	return $out . '</ul></nav>';
} );

add_shortcode( 'sm_menu_search', function () {
	return '<div class="sm-search" role="search">'
		. '<label class="screen-reader-text" for="sm-search-input">Search the Schnitz menu</label>'
		. '<input id="sm-search-input" type="search" placeholder="Search the menu - try &quot;parma&quot; or &quot;kids&quot;" autocomplete="off">'
		. '<p class="sm-search__status" aria-live="polite"></p>'
		. '</div>';
} );

add_shortcode( 'sm_print', function () {
	return '<button type="button" class="sm-btn sm-btn--ghost sm-print">' . sm_icon( 'print' ) . ' Print this menu</button>';
} );

/* ---------------------------------------------------------------------------
 * Tables
 * ------------------------------------------------------------------------- */

add_shortcode( 'sm_price_table', function ( $atts ) {
	$atts = shortcode_atts( array(
		'cat'     => '',
		'builder' => 'yes',
		'intro'   => 'yes',
	), $atts );

	$out = '';
	foreach ( sm_categories( $atts['cat'] ) as $cat ) {
		$out .= '<div class="sm-table-block" id="sm-cat-' . esc_attr( $cat['slug'] ) . '">';
		if ( 'yes' === $atts['intro'] && ! empty( $cat['intro'] ) ) {
			$out .= '<p class="sm-table-intro">' . esc_html( $cat['intro'] ) . '</p>';
		}
		$out .= '<div class="sm-table-scroll"><table class="sm-table" data-sm-sortable>';
		$out .= '<caption class="screen-reader-text">Schnitz ' . esc_html( $cat['name'] ) . ' prices and calories (' . esc_html( sm_updated_label() ) . ')</caption>';
		$out .= '<thead><tr><th scope="col">Item</th><th scope="col" class="sm-col-desc">Description</th>'
			. '<th scope="col" data-sort="num">Calories</th><th scope="col" data-sort="num">Price (AUD)</th>';
		if ( 'yes' === $atts['builder'] ) {
			$out .= '<th scope="col" class="sm-col-add"><span class="screen-reader-text">Add to meal</span></th>';
		}
		$out .= '</tr></thead><tbody>';
		foreach ( $cat['items'] as $item ) {
			$kcal  = isset( $item['kcal'] ) ? $item['kcal'] : null;
			$price = isset( $item['price'] ) ? $item['price'] : null;
			$tags  = '';
			foreach ( (array) ( isset( $item['tags'] ) ? $item['tags'] : array() ) as $tag ) {
				$tags .= ' <span class="sm-tag sm-tag--' . esc_attr( $tag ) . '">' . esc_html( $tag ) . '</span>';
			}
			$out .= '<tr data-name="' . esc_attr( strtolower( $item['name'] . ' ' . $item['desc'] . ' ' . $cat['name'] ) ) . '"'
				. ' data-kcal="' . esc_attr( null === $kcal ? '' : (int) $kcal ) . '"'
				. ' data-price="' . esc_attr( null === $price ? '' : (float) $price ) . '">';
			$out .= '<th scope="row">' . esc_html( $item['name'] ) . $tags . '</th>';
			$out .= '<td class="sm-col-desc">' . esc_html( $item['desc'] ) . '</td>';
			$out .= '<td>' . sm_kcal_html( $kcal ) . '</td>';
			$out .= '<td class="sm-price">' . sm_price_html( $price ) . '</td>';
			if ( 'yes' === $atts['builder'] ) {
				$out .= '<td class="sm-col-add"><button type="button" class="sm-add" aria-label="Add ' . esc_attr( $item['name'] ) . ' to my meal">+</button></td>';
			}
			$out .= '</tr>';
		}
		$out .= '</tbody></table></div></div>';
	}
	return $out;
} );

add_shortcode( 'sm_meal_builder', function () {
	return '<aside class="sm-builder" aria-label="Meal builder" hidden>'
		. '<div class="sm-builder__head"><strong>My Schnitz meal</strong><button type="button" class="sm-builder__clear">Clear</button></div>'
		. '<ul class="sm-builder__list"></ul>'
		. '<div class="sm-builder__totals"><span>Total: <b class="sm-builder__price">$0.00</b> <small>(approx.)</small></span>'
		. '<span><b class="sm-builder__kcal">0</b> kcal<small class="sm-builder__unknown"></small></span></div>'
		. '</aside>';
} );

add_shortcode( 'sm_calorie_chart', function ( $atts ) {
	$atts  = shortcode_atts( array( 'top' => 10 ), $atts );
	$items = array_filter( sm_all_items(), function ( $i ) {
		return ! empty( $i['kcal'] );
	} );
	usort( $items, function ( $a, $b ) {
		return $b['kcal'] - $a['kcal'];
	} );
	$items = array_slice( $items, 0, max( 1, (int) $atts['top'] ) );
	if ( ! $items ) {
		return '';
	}
	$max = $items[0]['kcal'];
	$out = '<figure class="sm-chart"><figcaption>Schnitz items by calories (highest first)</figcaption><ol>';
	foreach ( $items as $item ) {
		$pct  = round( $item['kcal'] / $max * 100 );
		$out .= '<li><span class="sm-chart__label">' . esc_html( $item['name'] ) . '</span>'
			. '<span class="sm-chart__bar" style="--w:' . esc_attr( $pct ) . '%"><span>' . esc_html( number_format( $item['kcal'] ) ) . ' kcal</span></span></li>';
	}
	return $out . '</ol></figure>';
} );

add_shortcode( 'sm_nutrition_table', function () {
	$out = '<div class="sm-table-scroll"><table class="sm-table" data-sm-sortable><thead><tr>'
		. '<th scope="col">Item</th><th scope="col">Category</th><th scope="col" data-sort="num">Calories</th><th scope="col" data-sort="num">Kilojoules</th>'
		. '</tr></thead><tbody>';
	foreach ( sm_all_items() as $item ) {
		if ( null === $item['kcal'] || '' === $item['kcal'] ) {
			continue;
		}
		$out .= '<tr data-name="' . esc_attr( strtolower( $item['name'] ) ) . '"><th scope="row">' . esc_html( $item['name'] ) . '</th>'
			. '<td>' . esc_html( $item['category'] ) . '</td>'
			. '<td>' . sm_kcal_html( $item['kcal'] ) . '</td>'
			. '<td>' . esc_html( number_format( round( $item['kcal'] * 4.184 ) ) ) . ' kJ</td></tr>';
	}
	return $out . '</tbody></table></div>';
} );

add_shortcode( 'sm_allergens', function () {
	$data = sm_data();
	if ( empty( $data['allergens'] ) ) {
		return '';
	}
	$a      = $data['allergens'];
	$labels = array(
		'yes'   => 'Contains',
		'no'    => 'Not listed',
		'check' => 'Check in store',
	);
	$out = '<div class="sm-table-scroll"><table class="sm-table sm-allergens"><thead><tr><th scope="col">Protein / coating</th>';
	foreach ( $a['columns'] as $col ) {
		$out .= '<th scope="col">' . esc_html( $col ) . '</th>';
	}
	$out .= '<th scope="col">Notes</th></tr></thead><tbody>';
	foreach ( $a['rows'] as $row ) {
		$out .= '<tr><th scope="row">' . esc_html( $row['name'] ) . '</th>';
		foreach ( $row['values'] as $i => $val ) {
			$val  = isset( $labels[ $val ] ) ? $val : 'check';
			$out .= '<td><span class="sm-dot sm-dot--' . esc_attr( $val ) . '" title="' . esc_attr( $labels[ $val ] ) . '"></span>'
				. '<span class="screen-reader-text">' . esc_html( $a['columns'][ $i ] . ': ' . $labels[ $val ] ) . '</span></td>';
		}
		$out .= '<td class="sm-note">' . esc_html( $row['note'] ) . '</td></tr>';
	}
	$out .= '</tbody></table></div><p class="sm-legend">'
		. '<span><span class="sm-dot sm-dot--yes"></span> Contains</span>'
		. '<span><span class="sm-dot sm-dot--no"></span> Not listed</span>'
		. '<span><span class="sm-dot sm-dot--check"></span> Check in store</span></p>';
	if ( ! empty( $a['source'] ) ) {
		$out .= '<p class="sm-small">Source: <a href="' . esc_url( $a['source'] ) . '" rel="nofollow noopener" target="_blank">official Schnitz allergen chart</a>. Recipes change - always confirm with your store.</p>';
	}
	return $out;
} );

add_shortcode( 'sm_deals', function () {
	$data = sm_data();
	if ( empty( $data['deals'] ) ) {
		return '';
	}
	$out = '<div class="sm-table-scroll"><table class="sm-table"><thead><tr><th scope="col">Deal</th><th scope="col">What you get</th><th scope="col">Price (AUD)</th><th scope="col">Last seen</th></tr></thead><tbody>';
	foreach ( $data['deals'] as $deal ) {
		$out .= '<tr><th scope="row">' . esc_html( $deal['name'] ) . '</th><td>' . esc_html( $deal['desc'] ) . '</td>'
			. '<td class="sm-price">' . sm_price_html( $deal['price'] ) . '</td><td>' . esc_html( $deal['seen'] ) . '</td></tr>';
	}
	return $out . '</tbody></table></div>';
} );

/* ---------------------------------------------------------------------------
 * FAQ + schema
 * ------------------------------------------------------------------------- */

add_shortcode( 'sm_faq', function ( $atts ) {
	$atts = shortcode_atts( array(
		'set'    => 'main',
		'limit'  => 0,
		'schema' => 'yes',
	), $atts );
	$data = sm_data();
	$faqs = isset( $data['faqs'][ $atts['set'] ] ) ? $data['faqs'][ $atts['set'] ] : array();
	if ( (int) $atts['limit'] > 0 ) {
		$faqs = array_slice( $faqs, 0, (int) $atts['limit'] );
	}
	if ( ! $faqs ) {
		return '';
	}

	$out    = '<div class="sm-faq">';
	$schema = array(
		'@context'   => 'https://schema.org',
		'@type'      => 'FAQPage',
		'mainEntity' => array(),
	);
	foreach ( $faqs as $i => $faq ) {
		$out .= '<details class="sm-faq__item"' . ( 0 === $i ? ' open' : '' ) . '><summary>' . esc_html( $faq['q'] ) . '</summary>'
			. '<div class="sm-faq__a"><p>' . esc_html( $faq['a'] ) . '</p></div></details>';

		$schema['mainEntity'][] = array(
			'@type'          => 'Question',
			'name'           => $faq['q'],
			'acceptedAnswer' => array(
				'@type' => 'Answer',
				'text'  => $faq['a'],
			),
		);
	}
	$out .= '</div>';
	if ( 'yes' === $atts['schema'] ) {
		$out .= '<script type="application/ld+json">' . wp_json_encode( $schema ) . '</script>';
	}
	return $out;
} );

add_shortcode( 'sm_menu_schema', function () {
	$sections = array();
	foreach ( sm_categories() as $cat ) {
		$items = array();
		foreach ( $cat['items'] as $item ) {
			$entry = array(
				'@type'       => 'MenuItem',
				'name'        => $item['name'],
				'description' => $item['desc'],
			);
			if ( ! empty( $item['price'] ) ) {
				$entry['offers'] = array(
					'@type'         => 'Offer',
					'price'         => number_format( (float) $item['price'], 2, '.', '' ),
					'priceCurrency' => 'AUD',
				);
			}
			if ( ! empty( $item['kcal'] ) ) {
				$entry['nutrition'] = array(
					'@type'    => 'NutritionInformation',
					'calories' => (int) $item['kcal'] . ' calories',
				);
			}
			$items[] = $entry;
		}
		$sections[] = array(
			'@type'       => 'MenuSection',
			'name'        => $cat['name'],
			'hasMenuItem' => $items,
		);
	}
	$schema = array(
		'@context'       => 'https://schema.org',
		'@type'          => 'Menu',
		'name'           => 'Schnitz Menu Australia (unofficial guide)',
		'inLanguage'     => 'en-AU',
		'hasMenuSection' => $sections,
	);
	return '<script type="application/ld+json">' . wp_json_encode( $schema ) . '</script>';
} );

/* ---------------------------------------------------------------------------
 * Calls to action, related pages, disclaimer
 * ------------------------------------------------------------------------- */

/**
 * Order buttons HTML. Affiliate links come from Appearance > Schnitz Menu Data.
 *
 * @return string
 */
function sm_order_buttons() {
	$links = array(
		'Order on Menulog'   => get_option( 'sm_menulog_url', '' ),
		'Order on Uber Eats' => get_option( 'sm_ubereats_url', '' ),
		'Order on DoorDash'  => get_option( 'sm_doordash_url', '' ),
	);
	$out = '<div class="sm-order">';
	foreach ( $links as $label => $url ) {
		if ( $url ) {
			$out .= '<a class="sm-btn" href="' . esc_url( $url ) . '" rel="sponsored nofollow noopener" target="_blank">' . sm_icon( 'bag' ) . ' ' . esc_html( $label ) . '</a>';
		}
	}
	$out .= '<a class="sm-btn sm-btn--ghost" href="' . esc_url( home_url( '/schnitz-menu/' ) ) . '">' . sm_icon( 'menu' ) . ' See the full menu</a>';
	return $out . '</div>';
}
add_shortcode( 'sm_order', 'sm_order_buttons' );

add_shortcode( 'sm_related', function ( $atts ) {
	$atts  = shortcode_atts( array( 'pages' => '' ), $atts );
	$pages = sm_site_pages();
	$slugs = $atts['pages'] ? array_map( 'trim', explode( ',', $atts['pages'] ) ) : array_keys( $pages );
	$out   = '<div class="sm-related">';
	foreach ( $slugs as $slug ) {
		if ( ! isset( $pages[ $slug ] ) ) {
			continue;
		}
		list( $title, $desc, $icon ) = $pages[ $slug ];
		$out .= '<a class="sm-related__card" href="' . esc_url( home_url( '/' . $slug . '/' ) ) . '">'
			. sm_icon( $icon ) . '<strong>' . esc_html( $title ) . '</strong><span>' . esc_html( $desc ) . '</span></a>';
	}
	return $out . '</div>';
} );

/**
 * Disclaimer text.
 *
 * @return string
 */
function sm_disclaimer_html() {
	return '<p class="sm-disclaimer"><strong>Disclaimer:</strong> SchnitzMenu.com is an unofficial, independent guide. We are not affiliated with, endorsed by, or sponsored by Schnitz International Pty Ltd. All prices are approximate, may vary by location and date, and are shown for information only. Always confirm current prices and allergen information directly with your local Schnitz restaurant.</p>';
}
add_shortcode( 'sm_disclaimer', 'sm_disclaimer_html' );
