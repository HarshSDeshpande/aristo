//! Built-in source language selection shared by discovery and CLI detection.

mod registry;

pub use registry::{language_for_extension, SourceLanguage};
