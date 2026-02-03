use super::common::*;
use super::run_config::RunConfig;
use binrw;
use binrw::{BinReaderExt, BinWriterExt};
use rayon::prelude::*;
use serde_json::Value;
use std::error::Error;
use std::fs::File;
use std::io;
use std::io::{BufWriter, Read, Seek, SeekFrom, Write};
use std::path::PathBuf;
use std::str::FromStr;
use std::time::Instant;


pub trait GenerateSnifferObservations {
    fn generate_sniffer_data(&self);
    fn load_sniffer_observations_binary(&self) -> Vec<ObservationSample>;
    fn sniffer_observations_binary_filename(&self) -> PathBuf;
    fn sniffer_locations_filename(&self) -> PathBuf;
}

impl<'a> GenerateSnifferObservations for RunConfig<'a> {
    fn generate_sniffer_data(&self) {
        println!("\n\n ==* running task: generate_sniffer_observations");

        let start = Instant::now();
        println!(
            "loading user samples from: {:?}",
            self.user_sample_filename()
        );
        let user_samples =
            load_user_samples(self.user_sample_filename().to_str().unwrap()).unwrap();
        println!("loaded {} user samples", user_samples.len());

        let sniffer_locations =
            load_sniffer_locations(self.sniffer_locations_filename().to_str().unwrap()).unwrap();
        println!("loaded {} sniffer locations", sniffer_locations.len());

        let elapsed = start.elapsed();
        println!("load elapsed: {:?}", elapsed);

        let compute_start = Instant::now();
        let observation_samples = generate_observation_samples(
            &sniffer_locations,
            &user_samples,
            self.ble_range_squared,
            self.wifi_range_squared,
            self.lte_range_squared,
        );
        let compute_elapsed = compute_start.elapsed();
        println!("compute elapsed: {:?}", compute_elapsed);

        let save_start = Instant::now();
        let saved_count = save_observations_binary(
            self.sniffer_observations_binary_filename()
                .to_str()
                .unwrap(),
            &sniffer_locations,
            &observation_samples,
            &user_samples,
            self.ble_range_squared,
            self.wifi_range_squared,
            self.lte_range_squared,
        );
        println!("save {:?} observations", saved_count);
        let save_elapsed = save_start.elapsed();
        println!("save elapsed: {:?}", save_elapsed);
    }

    fn load_sniffer_observations_binary(&self) -> Vec<ObservationSample> {
        load_observations_binary(
            self.sniffer_observations_binary_filename()
                .to_str()
                .unwrap(),
        )
    }

    fn sniffer_observations_binary_filename(&self) -> PathBuf {
        self.dedicated_data_dir()
            .join(format!("sniffed_data_{}.bin", self.name))
    }

    fn sniffer_locations_filename(&self) -> PathBuf {
        self.root_dir
            .join("sniffer_location")
            .join("full_coverage_wifi_sniffer_location.json")
    }
}

pub fn load_user_samples(filename: &str) -> Result<Vec<UserTraceSample>, Box<dyn Error>> {
    let mut reader = csv::Reader::from_path(filename)?;
    let mut samples: Vec<UserTraceSample> = Vec::new();
    for record in reader.records() {
        let line = record?;
        samples.push(UserTraceSample {
            timestep: f32::from_str(&line[0]).unwrap() as u32,
            user_id: String::from(&line[1]),
            loc: Location {
                x: f32::from_str(&line[2]).unwrap(),
                y: f32::from_str(&line[3]).unwrap(),
            },
            ble_id: String::from(&line[4]),
            wifi_id: String::from(&line[5]),
            lte_id: String::from(&line[6]),
            transmit_ble: bool::from_str(&line[7]).unwrap(),
            transmit_wifi: bool::from_str(&line[8]).unwrap(),
            transmit_lte: bool::from_str(&line[9]).unwrap(),
        })
    }

    Ok(samples)
}

pub fn save_observations_binary(
    filename: &str,
    sniffers: &[Sniffer],
    observations: &[Vec<usize>],
    user_samples: &[UserTraceSample],
    ble_range_squared: f32,
    wifi_range_squared: f32,
    lte_range_squared: f32,
) -> u64 {
    let mut writer = io::BufWriter::new(File::create(filename).unwrap());
    writer.write_le(&0u64).unwrap();

    /// Write the base info that do not change in relation to
    /// the protocol over which the observation was made.
    fn write_base_info<T: Write + Seek>(
        w: &mut BufWriter<T>,
        s: &Sniffer,
        u: &UserTraceSample,
        distance: f32,
    ) {
        // write fields in order
        w.write_le(&u.timestep).unwrap();

        let user_id_bytes = u.user_id.as_bytes();
        let user_id_bytes_len = user_id_bytes.len() as u8;
        w.write_le(&user_id_bytes_len).unwrap();
        w.write(user_id_bytes).unwrap();

        w.write_le(&distance).unwrap();
        w.write_le(&s.id).unwrap();

        w.write_le(&s.loc.x).unwrap();
        w.write_le(&s.loc.y).unwrap();

        w.write_le(&u.loc.x).unwrap();
        w.write_le(&u.loc.y).unwrap();
    }

    /// Write protocol-specific info.
    fn write_protocol_info<T: Write + Seek>(
        w: &mut BufWriter<T>,
        s: &Sniffer,
        p: ObservedProtocol,
        device_id: &str,
    ) {
        // write protocol
        let proc_id = p as u8;
        w.write_le(&proc_id).unwrap();

        // write protocol id
        let device_id_bytes = device_id.as_bytes();
        let device_id_bytes_len = device_id_bytes.len() as u8;
        w.write_le(&device_id_bytes_len).unwrap();
        w.write(device_id_bytes).unwrap();
    }

    let mut count: u64 = 0;
    for (s, obs) in sniffers.iter().zip(observations) {
        for ui in obs {
            // fetch the corresponding user sample
            let u = &user_samples[*ui];
            let distance = distance_squared_between(&u.loc, &s.loc).sqrt();

            // check for protocol transmission
            if u.transmit_ble && distance < ble_range_squared {
                // make sure to write a complete record every time
                count += 1;

                // write base info
                write_base_info(&mut writer, &s, &u, distance);

                // write BLE data
                write_protocol_info(&mut writer, &s, ObservedProtocol::BLE, &u.ble_id);
            }

            if u.transmit_wifi && distance < wifi_range_squared {
                // make sure to write a complete record every time
                count += 1;

                // write base info
                write_base_info(&mut writer, &s, &u, distance);

                // write BLE data
                write_protocol_info(&mut writer, &s, ObservedProtocol::WIFI, &u.wifi_id);
            }

            if u.transmit_lte && distance < lte_range_squared {
                // make sure to write a complete record every time
                count += 1;

                // write base info
                write_base_info(&mut writer, &s, &u, distance);

                // write BLE data
                write_protocol_info(&mut writer, &s, ObservedProtocol::LTE, &u.lte_id);
            }
        }
    }

    writer.seek(SeekFrom::Start(0)).unwrap();
    writer.write_le(&count).unwrap();
    writer.flush().unwrap();

    count
}

pub fn load_observations_binary(filename: &str) -> Vec<ObservationSample> {
    let mut reader = binrw::io::BufReader::new(File::open(filename).unwrap());
    let len = reader.read_le::<u64>().unwrap() as usize;
    let mut observations = Vec::<ObservationSample>::with_capacity(len as usize);

    let mut buf = [0u8; 256];
    for i in 0..len {
        let ts = reader.read_le::<u32>().unwrap();

        let user_id_len = reader.read_le::<u8>().unwrap() as usize;
        reader.read_exact(&mut buf[0..user_id_len]).unwrap();
        let user_id = std::str::from_utf8(&buf[0..user_id_len])
            .unwrap()
            .to_string();

        let distance = reader.read_le::<f32>().unwrap();
        let sniffer_id = reader.read_le::<u16>().unwrap();
        let sniffer_x = reader.read_le::<f32>().unwrap();
        let sniffer_y = reader.read_le::<f32>().unwrap();
        let user_x = reader.read_le::<f32>().unwrap();
        let user_y = reader.read_le::<f32>().unwrap();

        let protocol = match reader.read_le::<u8>().unwrap() {
            0 => ObservedProtocol::BLE,
            1 => ObservedProtocol::WIFI,
            2 => ObservedProtocol::LTE,
            _ => panic!("unknown observation protocol"),
        };

        let device_id_len = reader.read_le::<u8>().unwrap() as usize;
        reader.read_exact(&mut buf[0..device_id_len]).unwrap();
        let device_id = std::str::from_utf8(&buf[0..device_id_len])
            .unwrap()
            .to_string();

        observations.push(ObservationSample {
            timestep: ts,
            user_id,
            device_id,
            user_loc: Location {
                x: user_x,
                y: user_y,
            },
            sniffer: Sniffer {
                id: sniffer_id,
                loc: Location {
                    x: sniffer_x,
                    y: sniffer_y,
                },
            },
            distance,
            protocol,
        })
    }

    observations
}

pub fn load_sniffer_locations(filename: &str) -> Result<Vec<Sniffer>, Box<dyn Error>> {
    let json_src = std::fs::read_to_string(filename).unwrap();
    let src: Value = serde_json::from_str(&json_src).unwrap();

    let mut sniffers: Vec<Sniffer> = Vec::new();
    let mut count: u16 = 0;
    for s in src["sniffer_location"].as_array().unwrap() {
        let ss = s.as_array().unwrap();
        sniffers.push(Sniffer {
            id: count,
            loc: Location {
                x: ss[0].as_f64().unwrap() as f32,
                y: ss[1].as_f64().unwrap() as f32,
            },
        });

        count += 1
    }

    Ok(sniffers)
}

pub fn generate_observation_samples(
    sniffers: &[Sniffer],
    user_samples: &[UserTraceSample],
    ble_range_squared: f32,
    wifi_range_squared: f32,
    lte_range_squared: f32,
) -> Vec<Vec<usize>> {
    sniffers
        .par_iter()
        .map(|s| {
            generate_observation_samples_for_one(
                s,
                user_samples,
                ble_range_squared,
                wifi_range_squared,
                lte_range_squared,
            )
        })
        .collect()
}

pub fn generate_observation_samples_for_one(
    sniffer: &Sniffer,
    user_samples: &[UserTraceSample],
    ble_range_squared: f32,
    wifi_range_squared: f32,
    lte_range_squared: f32,
) -> Vec<usize> {
    let mut observation_samples: Vec<usize> = Vec::new();
    for (i, sample) in user_samples.iter().enumerate() {
        let distance = distance_squared_between(&sniffer.loc, &sample.loc);

        let can_be_observed = (sample.transmit_ble && distance < ble_range_squared)
            || (sample.transmit_wifi && distance < wifi_range_squared)
            || (sample.transmit_lte && distance < lte_range_squared);

        if can_be_observed {
            observation_samples.push(i);
        }
    }

    observation_samples
}
