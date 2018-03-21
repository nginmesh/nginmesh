extern crate ngx_rust;

use ngx_rust::bindings:: { ngx_int_t, ngx_str_t } ;


#[repr(C)]
pub struct ngx_http_mixer_main_conf_t {

    pub mixer_server: ngx_str_t,
    pub mixer_port: ngx_int_t
}


