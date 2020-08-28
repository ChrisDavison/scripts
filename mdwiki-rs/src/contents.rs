use std::fs;
use std::path::PathBuf;

pub fn directory_as_markdown_links(path: &PathBuf) -> String {
    let mut files = String::new();
    let mut dirs = String::new();
    for entry in fs::read_dir(path).unwrap() {
        let entry = entry.unwrap();
        let path = entry.path();
        let link_str = format!(
            "\n- [{}](./view/{})",
            path.file_name().unwrap().to_string_lossy(),
            path.to_string_lossy()
        );
        if path.is_dir() {
            dirs.push_str(link_str.as_ref())
        } else {
            if path.extension().unwrap().to_string_lossy() == "md" {
                files.push_str(link_str.as_ref())
            }
        }
    }

    format!(
        "## directories\n\n{}\n\n---\n\n## files\n\n{}\n",
        dirs, files
    )
}
