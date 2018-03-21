
use std::sync::mpsc::{channel};
use std::sync::Mutex;




use ngx_rust::bindings:: { ngx_array_t };
use ngx_rust::bindings::ngx_http_request_s;
use ngx_rust::bindings::ngx_http_upstream_state_t;

use ngx_mixer_transport::attribute::attr_wrapper::AttributeWrapper;
use ngx_mixer_transport::attribute::global_dict::{ RESPONSE_DURATION };


use super::message::Channels;
use super::message::MixerInfo;

use ngx::main_config::ngx_http_mixer_main_conf_t;
use ngx::server_config::ngx_http_mixer_srv_conf_t;
use ngx::config::MixerConfig;
use kafka::producer::{Producer, Record, RequiredAcks};
use std::fmt::Write;
use std::time::Duration;


// initialize channel that can be shared
lazy_static! {
    static ref CHANNELS: Channels<MixerInfo> = {
        let (tx, rx) = channel();

        Channels {
            tx: Mutex::new(tx),
            rx: Mutex::new(rx),
        }
    };
}

fn send_stat(message: &str) {
    
    lazy_static!  {
         static ref MSG_PRODUCER: Mutex<Producer> = Mutex::new(Producer::from_hosts(vec!("broker.kafka:9092".to_owned()))
                .with_ack_timeout(Duration::from_secs(1))
                .with_required_acks(RequiredAcks::One)
                .create()
                .unwrap());

    }
   
    let mut buf = String::with_capacity(2);
    let _ = write!(&mut buf, "{}", message); 
    MSG_PRODUCER.lock().unwrap().send(&Record::from_value("test", buf.as_bytes())).unwrap();
    ngx_event_debug!("send event to kafka topic test");

}


// background activy for report.
// receives report attributes and send out to mixer
pub fn mixer_report_background()  {

    let rx = CHANNELS.rx.lock().unwrap();
    let mut producer: Producer  = Producer::from_hosts(vec!("broker.kafka:9092".to_owned()))
                .with_ack_timeout(Duration::from_secs(1))
                .with_required_acks(RequiredAcks::One)
                .create()
                .unwrap();


    loop {
        ngx_event_debug!("mixer report  thread waiting");
        let info = rx.recv().unwrap();
        ngx_event_debug!("mixer report thread woke up");

        
        let mut buf = String::with_capacity(2);
        let _ = write!(&mut buf, "{}", info.attributes); 
        producer.send(&Record::from_value("test", buf.as_bytes())).unwrap();
        ngx_event_debug!("send event to kafka topic test");

        /*
        let client = MixerClient::new_plain( &info.server_name, info.server_port , Default::default()).expect("init");

        let mut req = ReportRequest::new();
        let mut rf = RepeatedField::default();
        rf.push(info.attributes);
        req.set_attributes(rf);

        let resp = client.report(RequestOptions::new(), req);

        let result = resp.wait();
        */

        ngx_event_debug!("mixer report thread: finished sending to kafka");
    }
}


// send to background thread using channels
#[allow(unused_must_use)]
fn send_dispatcher(request: &ngx_http_request_s,main_config: &ngx_http_mixer_main_conf_t, attr: AttributeWrapper)  {

    let server_name = main_config.mixer_server.to_str();
    let server_port = main_config.mixer_port as u16;

    /*
    let tx = CHANNELS.tx.lock().unwrap().clone();
    let info = MixerInfo { server_name: String::from(server_name), server_port: server_port, attributes: attr.to_string()};
    tx.send(info.clone());
    */
    send_stat(&attr.to_string());

    ngx_http_debug!(request,"finish sending to kafer");

}


// Total Upstream response Time Calculation Function Start

fn upstream_response_time_calculation( upstream_states: *const ngx_array_t ) -> i64 {

    unsafe {

        let upstream_value = *upstream_states;
        let upstream_response_time_list = upstream_value.elts;
        let upstream_response_time_n = upstream_value.nelts as isize;
        let upstream_response_time_size = upstream_value.size as isize;
        let mut upstream_response_time_total:i64 = 0;
        for i in 0..upstream_response_time_n as isize {

            let upstream_response_time_ptr = upstream_response_time_list.offset(i*upstream_response_time_size) as *mut ngx_http_upstream_state_t;
            let upstream_response_time_value = (*upstream_response_time_ptr).response_time as i64;
            upstream_response_time_total = upstream_response_time_total + upstream_response_time_value;

        }

        return upstream_response_time_total;
    }
}


#[no_mangle]
pub extern fn nginmesh_mixer_report_handler(request: &ngx_http_request_s,main_config: &ngx_http_mixer_main_conf_t,
    srv_conf: &ngx_http_mixer_srv_conf_t)  {


    let mut attr = AttributeWrapper::new();
    srv_conf.process_istio_attr(&mut attr);
    request.process_istio_attr(&mut attr);
    attr.insert_int64_attribute(RESPONSE_DURATION, upstream_response_time_calculation(request.upstream_states));
    
    let headers_out =  &request.headers_out;
    headers_out.process_istio_attr(&mut attr);

    send_dispatcher(request,main_config, attr)   

}



