#!/usr/bin/env python3
import argparse
import sys
import os
import logging
from pathlib import Path

# --- Local Imports ---
# Assume these modules exist and have the necessary functions/classes
# (These were implemented in previous tasks)
from .config_loader import ConfigLoader # Task 2
from .file_manager import FileManager # Task 3 & 4
from .utils.hashing import calculate_content_hash, calculate_yaml_hash # Task 5
from .processing.change_detection import compare_hashes, determine_action, ActionType # Task 14
from .processing.markdown_processor import MarkdownProcessor # Task 6
from .services.translation_service import TranslationService # Task 8
from .utils.types import TranslationMap, TextSegment, SegmentType # Task 7

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('translation-cli')

def parse_args():
    parser = argparse.ArgumentParser(description='Markdown Content Translator Tool')
    
    # Adjusted defaults to be relative to project root
    parser.add_argument(
        '-s', '--settings', 
        default='config/settings.txt', 
        help='Path to settings file relative to translation-py directory'
    )
    parser.add_argument(
        '-e', '--env', 
        default='config/translate.env', 
        help='Path to environment file relative to translation-py directory'
    )
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help='Enable verbose (DEBUG) output'
    )
    
    return parser.parse_args()

def get_project_root() -> Path:
    """Find the project root directory containing the 'translation-py' directory."""
    current_dir = Path(__file__).parent
    # Traverse up until we find a directory containing 'translation-py'
    # This assumes a standard project structure
    while not (current_dir / 'translation-py').exists():
        if current_dir.parent == current_dir:
            # Reached filesystem root, cannot find project root
            raise FileNotFoundError("Could not determine project root. Ensure script is run within the project structure.")
        current_dir = current_dir.parent
    # Adjust based on where translation-py actually lives relative to the discovered root
    # If this script is in translation-py/src, the root is two levels up
    project_root = Path(__file__).parent.parent.parent
    # A more robust way might involve looking for a marker file (e.g., .git, pyproject.toml)
    # For now, assume standard structure
    # Hardcoding for demo purposes if above fails:
    # project_root = Path("C:/Users/Marc Bielert/Github/circuswiki-dev") 
    logger.info(f"Determined project root: {project_root}")
    return project_root

def main():
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.info("Verbose mode enabled.")

    try:
        # Determine project root relative to this script
        project_root = get_project_root()
        # Construct absolute paths for config relative to project root
        # Assuming script is in translation-py/src
        translation_py_root = project_root / 'translation-py'
        settings_path = (translation_py_root / args.settings).resolve()
        env_path = (translation_py_root / args.env).resolve()
        
        logger.info(f"Using settings file: {settings_path}")
        logger.info(f"Using environment file: {env_path}")

        # --- 1. Load Configuration ---
        logger.info("Loading configuration...")
        config_loader = ConfigLoader(settings_path=str(settings_path), env_path=str(env_path))
        config_loader.load_config()
        logger.info("Configuration loaded successfully.")
        
        input_dir_rel = config_loader.settings.get('INPUT_DIR', 'docs') # Default relative to project root
        output_dir_rel = config_loader.settings.get('OUTPUT_DIR', 'translated_docs') # Default relative to project root

        # Resolve input/output dirs relative to project root
        input_dir = (project_root / input_dir_rel).resolve()
        output_dir = (project_root / output_dir_rel).resolve()

        logger.info(f"Input directory: {input_dir}")
        logger.info(f"Output directory: {output_dir}")

        # --- 2. Initialize Components ---
        file_manager = FileManager(str(input_dir), str(output_dir))
        markdown_processor = MarkdownProcessor(config_loader.settings) # Pass config to processor
        translation_service = TranslationService(config_loader) # Task 8

        # --- 3. Scan for Files ---
        logger.info(f"Scanning for Markdown files in {input_dir}...")
        markdown_files = file_manager.scan_markdown_files()
        logger.info(f"Found {len(markdown_files)} Markdown files.")

        if not markdown_files:
            logger.info("No Markdown files found to process.")
            return 0

        # --- 4. Process Each File ---
        processed_count = 0
        skipped_count = 0
        translation_count = 0
        yaml_update_count = 0
        error_count = 0

        for file_path in markdown_files:
            logger.info(f"Processing file: {file_path.relative_to(project_root)}")
            try:
                # --- 4a. Read File & Extract Frontmatter ---
                frontmatter, content = file_manager.read_markdown_with_frontmatter(file_path)
                if content is None: # If file read failed
                    logger.warning(f"Could not read or parse {file_path}. Skipping.")
                    error_count += 1
                    continue
                # Ensure frontmatter is a dict, even if empty or parsing failed slightly
                if frontmatter is None: 
                    frontmatter = {}

                # --- 4b. Calculate Hashes ---
                logger.debug(f"Calculating hashes for {file_path.name}")
                current_content_hash = calculate_content_hash(content)
                # Pass the *parsed* frontmatter dict to calculate_yaml_hash
                current_yaml_hash = calculate_yaml_hash(frontmatter)
                current_hashes = {
                    'content': current_content_hash,
                    'yaml': current_yaml_hash
                }
                logger.debug(f"Calculated Hashes - Content: {current_content_hash}, YAML: {current_yaml_hash}")

                # --- 4c. Compare Hashes & Determine Action (Task 14 Integration) ---
                comparison_result = compare_hashes(current_hashes, frontmatter)
                action = determine_action(comparison_result)

                # --- 4d. Execute Action ---
                if action == ActionType.SKIP:
                    logger.info(f"Skipping file (no changes detected): {file_path.name}")
                    skipped_count += 1
                    # Optionally update source hash even if skipped, if desired
                    # file_manager.update_file_hashes(file_path, current_content_hash, current_yaml_hash) 
                    pass # No further action needed
                
                elif action == ActionType.YAML_UPDATE:
                    logger.info(f"YAML update needed for: {file_path.name}")
                    # --- Placeholder for Task 15: YAML-only Update ---
                    # TODO: Implement YAML-only update logic (Task 15)
                    # - Read existing translations
                    # - Update only their frontmatter based on changes in source frontmatter
                    # - Rewrite translated files
                    logger.warning("YAML-only update not yet implemented (Task 15). Performing source hash update only.")
                    file_manager.update_file_hashes(file_path, current_content_hash, current_yaml_hash) 
                    yaml_update_count += 1
                    # -----------------------------------------------
                    
                elif action == ActionType.FULL_TRANSLATION:
                    logger.info(f"Full translation needed for: {file_path.name}")
                    
                    # --- Actual Full Translation Pipeline ---
                    # 1. Extract translatable segments (Task 7 & 13)
                    # Pass both content and frontmatter to the processor
                    translation_map = markdown_processor.extract_translatable_segments(content, frontmatter)
                    
                    if not translation_map.segments:
                        logger.info(f"No translatable segments found in {file_path.name}. Updating hash only.")
                        file_manager.update_file_hashes(file_path, current_hashes['content'], current_hashes['yaml']) # Task 12
                        processed_count += 1
                        continue # Skip to next file

                    # Prepare texts for batch translation
                    original_texts = [seg.text for seg in translation_map.segments]
                    
                    # 2. Translate segments for each target language (Task 8)
                    for lang in config_loader.get_target_languages():
                        logger.info(f"Translating {file_path.name} to {lang}...")
                        try:
                            translated_texts = translation_service.translate_batch(original_texts, lang)
                            
                            if len(translated_texts) != len(original_texts):
                                logger.error(f"Translation count mismatch for {lang}. Expected {len(original_texts)}, got {len(translated_texts)}. Skipping language.")
                                # Decide how to handle partial failure - skip lang? error out?
                                continue

                            # Create map of original_text -> translated_text for reassembly
                            translation_dict = dict(zip(original_texts, translated_texts))
                            
                            # Separate translated segments for body and YAML
                            translated_body_segments = {seg.path: translation_dict[seg.text] 
                                                      for seg in translation_map.segments if seg.type == SegmentType.MARKDOWN}
                            translated_yaml_fields = {seg.path.split(' > ')[-1]: translation_dict[seg.text] 
                                                    for seg in translation_map.segments if seg.type == SegmentType.YAML}

                            # 3. Reconstruct translated Markdown (Task 10)
                            # Pass only body segments for markdown reassembly
                            reconstructed_content = markdown_processor.reassemble_markdown(content, translated_body_segments)

                            # 4. Generate output frontmatter (Task 11 & 13)
                            output_frontmatter = file_manager.generate_frontmatter(
                                original_frontmatter=frontmatter, 
                                translated_fields=translated_yaml_fields, 
                                lang_code=lang, 
                                source_hashes=current_hashes # Pass current hashes
                            )
                            
                            # 5. Write output file (Task 11)
                            output_path = file_manager.get_output_path(file_path, lang)
                            file_manager.write_translated_file(output_path, output_frontmatter, reconstructed_content)
                            logger.info(f"Successfully wrote translated file: {output_path.relative_to(project_root)}")

                        except Exception as trans_err:
                            logger.error(f"Error translating or writing file {file_path.name} for language {lang}: {trans_err}", exc_info=True)
                            # Optionally increment a language-specific error count
                            continue # Continue to next language
                    
                    # 6. Update source file hashes *after* all languages are processed (Task 12)
                    file_manager.update_file_hashes(file_path, current_hashes['content'], current_hashes['yaml'])
                    translation_count += 1
                    # ---------------------------------------------
                    
                processed_count += 1

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}", exc_info=True)
                error_count += 1

        # --- 5. Summary --- 
        logger.info("--- Processing Summary ---")
        logger.info(f"Total files scanned: {len(markdown_files)}")
        logger.info(f"Files processed: {processed_count}")
        logger.info(f"Files skipped (no changes): {skipped_count}")
        logger.info(f"Files requiring full translation: {translation_count} (Placeholder)")
        logger.info(f"Files requiring YAML-only update: {yaml_update_count} (Placeholder)")
        logger.info(f"Errors encountered: {error_count}")
        logger.info("-------------------------")
        
        return 0 # Success

    except FileNotFoundError as e:
        logger.error(f"Configuration or directory error: {e}")
        return 1 # Indicate error
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")
        return 1 # Indicate error

if __name__ == "__main__":
    sys.exit(main()) 