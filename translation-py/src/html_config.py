from typing import List, Dict, Set
import logging

logger = logging.getLogger(__name__)

class HtmlProcessingConfig:
    """Holds configuration settings for HTML processing."""

    def __init__(self, config_data: Dict):
        """Initialize config from a dictionary (e.g., loaded from YAML)."""
        self.extract_content_tags: Set[str] = set(config_data.get('extract_content_tags', []))
        self.extract_attribute_tags: Dict[str, Set[str]] = {
            tag: set(attrs) 
            for tag, attrs in config_data.get('extract_attribute_tags', {}).items()
        }
        self.preserve_tags: Set[str] = set(config_data.get('preserve_tags', []))
        self.default_tag_behavior: str = config_data.get('default_tag_behavior', 'preserve')

        self._validate_config()
        logger.info("HtmlProcessingConfig initialized.")
        logger.debug(f"Extract Content Tags: {self.extract_content_tags}")
        logger.debug(f"Extract Attribute Tags: {self.extract_attribute_tags}")
        logger.debug(f"Preserve Tags: {self.preserve_tags}")
        logger.debug(f"Default Tag Behavior: {self.default_tag_behavior}")


    def _validate_config(self):
        """Performs basic validation checks on the loaded configuration."""
        overlapping_tags = (
            (self.extract_content_tags & self.preserve_tags) |
            (set(self.extract_attribute_tags.keys()) & self.preserve_tags)
        )
        if overlapping_tags:
            logger.warning(
                f"HTML Config Validation: Tags listed in both extract_* and preserve_tags: {overlapping_tags}. "
                f"Preserve will take precedence."
            )
            # Ensure preserve takes precedence by removing from extract lists
            self.extract_content_tags -= overlapping_tags
            for tag in overlapping_tags:
                 if tag in self.extract_attribute_tags:
                     del self.extract_attribute_tags[tag]

        if self.default_tag_behavior not in ['preserve', 'extract']:
            logger.warning(
                f"HTML Config Validation: Invalid default_tag_behavior '{self.default_tag_behavior}'. "
                f"Defaulting to 'preserve'."
            )
            self.default_tag_behavior = 'preserve'

    def should_extract_content(self, tag_name: str) -> bool:
        """Check if the content of a given tag should be extracted."""
        tag_name = tag_name.lower()
        if tag_name in self.preserve_tags:
            return False
        if tag_name in self.extract_content_tags:
            return True
        # Apply default behavior for unlisted tags
        return self.default_tag_behavior == 'extract'

    def should_preserve_tag(self, tag_name: str) -> bool:
        """Check if a given tag should be preserved entirely."""
        return tag_name.lower() in self.preserve_tags

    def get_extractable_attributes(self, tag_name: str) -> Set[str]:
        """Get the set of attributes to extract for a given tag."""
        tag_name = tag_name.lower()
        if tag_name in self.preserve_tags:
            return set() # No attributes extracted if tag is preserved
        return self.extract_attribute_tags.get(tag_name, set()) 