<?php
/**
 * Appearance > Schnitz Menu Data: edit prices, calories, FAQs, affiliate links
 * and the "Updated" date without touching theme files.
 *
 * @package schnitzmenu
 */

defined( 'ABSPATH' ) || exit;

/**
 * Register settings.
 */
function sm_register_settings() {
	register_setting( 'sm_settings', 'sm_updated', array( 'sanitize_callback' => 'sanitize_text_field' ) );
	register_setting( 'sm_settings', 'sm_menu_json', array( 'sanitize_callback' => 'sm_sanitize_json' ) );
	register_setting( 'sm_settings', 'sm_menulog_url', array( 'sanitize_callback' => 'esc_url_raw' ) );
	register_setting( 'sm_settings', 'sm_ubereats_url', array( 'sanitize_callback' => 'esc_url_raw' ) );
	register_setting( 'sm_settings', 'sm_doordash_url', array( 'sanitize_callback' => 'esc_url_raw' ) );
	register_setting( 'sm_settings', 'sm_sidebar_box', array(
		'sanitize_callback' => 'absint',
		'default'           => 1,
	) );
}
add_action( 'admin_init', 'sm_register_settings' );

/**
 * Keep the old data if the JSON doesn't parse, so a typo can't break the site.
 *
 * @param string $value Submitted JSON.
 * @return string
 */
function sm_sanitize_json( $value ) {
	$value = trim( (string) $value );
	if ( '' === $value ) {
		return ''; // Empty = use the bundled data/menu.json.
	}
	$decoded = json_decode( $value, true );
	if ( ! is_array( $decoded ) || empty( $decoded['categories'] ) ) {
		add_settings_error( 'sm_menu_json', 'sm_bad_json', 'Menu data was NOT saved: the JSON is invalid (' . json_last_error_msg() . '). Your previous data is still live.' );
		return get_option( 'sm_menu_json', '' );
	}
	return wp_json_encode( $decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
}

/**
 * Menu entry.
 */
function sm_admin_menu() {
	add_theme_page( 'Schnitz Menu Data', 'Schnitz Menu Data', 'manage_options', 'sm-data', 'sm_admin_page' );
}
add_action( 'admin_menu', 'sm_admin_menu' );

/**
 * Settings screen.
 */
function sm_admin_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$json = get_option( 'sm_menu_json', '' );
	if ( ! $json ) {
		$json = wp_json_encode( sm_default_data(), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	}
	?>
	<div class="wrap">
		<h1>Schnitz Menu Data</h1>
		<p>Everything in the price tables, calorie chart, allergen matrix and FAQs comes from here. Update it on the first of every month.</p>
		<?php settings_errors( 'sm_menu_json' ); ?>
		<form method="post" action="options.php">
			<?php settings_fields( 'sm_settings' ); ?>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row"><label for="sm_updated">"Updated" label</label></th>
					<td><input name="sm_updated" id="sm_updated" type="text" class="regular-text" value="<?php echo esc_attr( get_option( 'sm_updated', '' ) ); ?>" placeholder="<?php echo esc_attr( wp_date( 'F Y' ) ); ?>">
					<p class="description">Shown in the "Updated ..." badge on every page. Leave blank to use the date inside the data below.</p></td>
				</tr>
				<tr>
					<th scope="row"><label for="sm_menulog_url">Menulog affiliate link</label></th>
					<td><input name="sm_menulog_url" id="sm_menulog_url" type="url" class="regular-text" value="<?php echo esc_attr( get_option( 'sm_menulog_url', '' ) ); ?>"></td>
				</tr>
				<tr>
					<th scope="row"><label for="sm_ubereats_url">Uber Eats affiliate link</label></th>
					<td><input name="sm_ubereats_url" id="sm_ubereats_url" type="url" class="regular-text" value="<?php echo esc_attr( get_option( 'sm_ubereats_url', '' ) ); ?>"></td>
				</tr>
				<tr>
					<th scope="row"><label for="sm_doordash_url">DoorDash affiliate link</label></th>
					<td><input name="sm_doordash_url" id="sm_doordash_url" type="url" class="regular-text" value="<?php echo esc_attr( get_option( 'sm_doordash_url', '' ) ); ?>">
					<p class="description">Order buttons only appear once a link is filled in.</p></td>
				</tr>
				<tr>
					<th scope="row">Sidebar box</th>
					<td><label><input name="sm_sidebar_box" type="checkbox" value="1" <?php checked( get_option( 'sm_sidebar_box', 1 ) ); ?>> Show "Schnitz guides" links + order buttons under the sidebar widgets</label></td>
				</tr>
				<tr>
					<th scope="row"><label for="sm_menu_json">Menu data (JSON)</label></th>
					<td>
						<textarea name="sm_menu_json" id="sm_menu_json" rows="30" class="large-text code" spellcheck="false"><?php echo esc_textarea( $json ); ?></textarea>
						<p class="description">Use <code>null</code> for an unknown price or calorie count (shown as "Varies" / "&mdash;"). Clear the box and save to go back to the theme's bundled data. Invalid JSON is rejected and your old data stays live.</p>
					</td>
				</tr>
			</table>
			<?php submit_button(); ?>
		</form>

		<h2>Images</h2>
		<?php if ( isset( $_GET['sm_media_added'] ) ) : // phpcs:ignore WordPress.Security.NonceVerification.Recommended ?>
			<div class="notice notice-success"><p><?php echo esc_html( sprintf( '%d illustration(s) added to the Media Library.', absint( $_GET['sm_media_added'] ) ) ); // phpcs:ignore WordPress.Security.NonceVerification.Recommended ?></p></div>
		<?php endif; ?>
		<p>The theme ships original illustrations (WebP, 3-21 KB each). Copy them into the Media Library to use them in any Elementor Image widget - alt text is filled in for you. Already-copied images are skipped.</p>
		<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
			<input type="hidden" name="action" value="sm_import_media">
			<?php wp_nonce_field( 'sm_import_media' ); ?>
			<?php submit_button( 'Add illustrations to Media Library', 'secondary', 'submit', false ); ?>
		</form>
	</div>
	<?php
}
