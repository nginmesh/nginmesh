
use ngx_mixer_transport::attribute::attr_wrapper::AttributeWrapper;

pub trait MixerConfig {

    // convert and migrate values to istio attributes
    fn process_istio_attr(&self, attr: &mut AttributeWrapper);

}
