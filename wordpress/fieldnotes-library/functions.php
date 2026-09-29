<?php
/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 Ismail Habib
 */

add_action('after_setup_theme',function(){add_theme_support('title-tag');});
add_action('wp_enqueue_scripts',function(){wp_enqueue_style('fieldnotes',get_stylesheet_uri(),array(),'1.0.0');wp_enqueue_script('fieldnotes-bookmarks',get_template_directory_uri().'/bookmarks.js',array(),'1.0.0',true);});
function fn_saved(){return isset($_GET['saved']) && $_GET['saved']==='1';}
function fn_card($id){$slug=get_post_field('post_name',$id);$topic=get_post_meta($id,'fn_topic',true);$type=get_post_meta($id,'fn_type',true);$minutes=get_post_meta($id,'fn_minutes',true);$cls=array('API integration'=>'api','AI automation'=>'ai','Legacy software'=>'legacy','WordPress'=>'wp')[$topic]??'api';$symbol=array('api'=>'{ } ⇄ { }','ai'=>'✳ → ✓','legacy'=>'[ C++ ]','wp'=>'▤ → ↗')[$cls];?>
<article class="card" data-card="<?php echo esc_attr($slug); ?>"><div class="art <?php echo esc_attr($cls); ?>"><span class="symbol" aria-hidden="true"><?php echo esc_html($symbol); ?></span><button class="bookmark" data-bookmark="<?php echo esc_attr($slug); ?>" aria-pressed="false" aria-label="Save article">▢</button></div><div class="cardbody"><div class="tagline"><?php echo esc_html($topic.' / '.$type); ?></div><h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3><p><?php echo esc_html(get_the_excerpt($id)); ?></p><div class="cardfoot"><span><?php echo esc_html($minutes); ?> min read</span><a href="<?php echo esc_url(get_permalink($id)); ?>">Open note ↗</a></div></div></article>
<?php }
