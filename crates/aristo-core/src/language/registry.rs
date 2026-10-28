use crate::walk::extract::{extract_from_source, ExtractError, ExtractedAnnotation};
use crate::walk::extract_c::extract_from_c_source;

pub(crate) struct SourceLanguage {
    extensions: &'static [&'static str],
    extractor: fn(&str) -> Result<Vec<ExtractedAnnotation>, ExtractError>,
}

impl SourceLanguage {
    pub(crate) fn extract(&self, source: &str) -> Result<Vec<ExtractedAnnotation>, ExtractError> {
        (self.extractor)(source)
    }
}

static SOURCE_LANGUAGES: &[SourceLanguage] = &[
    SourceLanguage {
        extensions: &["rs"],
        extractor: extract_from_source,
    },
    SourceLanguage {
        extensions: &["c", "h"],
        extractor: extract_from_c_source,
    },
];

#[aristo::intent(
    "Both the annotation walk and the freshness preflight route their \
     extension check through this one function, so they can never disagree \
     on which files count as source. Filtering `.c`/`.h` in here but not in \
     the freshness walk would silently stop drift detection for C files — \
     they would be indexed once but never re-checked for staleness. `.h` is \
     treated as C.",
    verify = "test",
    id = "source_language_extension_set_is_single_authority"
)]
pub(crate) fn language_for_extension(ext: Option<&str>) -> Option<&'static SourceLanguage> {
    let ext = ext?;
    SOURCE_LANGUAGES
        .iter()
        .find(|language| language.extensions.contains(&ext))
}
