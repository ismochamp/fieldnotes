<?php
/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 Ismail Habib
 */

/* Plugin Name: Fieldnotes Content
Description: Editable knowledge resources and eight original field guides.
Version: 1.0.0
Author: Ismail Habib
License: MIT
License URI: https://opensource.org/license/mit/
*/
if(!defined('ABSPATH'))exit;
function fn_register(){register_post_type('fieldnote',array('label'=>'Fieldnotes','public'=>true,'show_in_rest'=>true,'supports'=>array('title','editor','excerpt','revisions'),'has_archive'=>true,'rewrite'=>array('slug'=>'articles'),'menu_icon'=>'dashicons-media-document'));}
add_action('init','fn_register');
register_activation_hook(__FILE__,function(){fn_register();$items=json_decode(file_get_contents(__DIR__.'/articles.json'),true);foreach($items as $a){if(get_page_by_path($a['slug'],OBJECT,'fieldnote'))continue;$body='<pre>'.esc_html($a['code']).'</pre>';foreach($a['sections'] as $s)$body.='<h2>'.esc_html($s[0]).'</h2><p>'.esc_html($s[1]).'</p>';$body.='<h2>Take this into your next project</h2><ul>';foreach($a['checklist'] as $item)$body.='<li>'.esc_html($item).'</li>';$body.='</ul>';$id=wp_insert_post(array('post_type'=>'fieldnote','post_status'=>'publish','post_name'=>$a['slug'],'post_title'=>$a['title'],'post_excerpt'=>$a['intro'],'post_content'=>$body));if($id&&!is_wp_error($id)){foreach(array('topic','type','minutes') as $key)update_post_meta($id,'fn_'.$key,$a[$key]);}}flush_rewrite_rules();});
register_deactivation_hook(__FILE__,function(){flush_rewrite_rules();});
add_action('add_meta_boxes',function(){add_meta_box('fn_details','Resource details',function($post){wp_nonce_field('fn_save','fn_nonce');foreach(array('topic'=>'Topic (API integration, AI automation, Legacy software, WordPress)','type'=>'Format','minutes'=>'Reading time in minutes') as $key=>$label)echo '<p><label>'.esc_html($label).'<br><input style="width:100%" name="fn_'.esc_attr($key).'" value="'.esc_attr(get_post_meta($post->ID,'fn_'.$key,true)).'"></label></p>';},'fieldnote','side');});
add_action('save_post_fieldnote',function($id){if(!isset($_POST['fn_nonce'])||!wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['fn_nonce'])),'fn_save')||!current_user_can('edit_post',$id)||(defined('DOING_AUTOSAVE')&&DOING_AUTOSAVE))return;foreach(array('topic','type','minutes') as $key){if(isset($_POST['fn_'.$key]))update_post_meta($id,'fn_'.$key,sanitize_text_field(wp_unslash($_POST['fn_'.$key])));}});
