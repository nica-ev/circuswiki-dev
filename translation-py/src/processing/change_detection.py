import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum, auto

logger = logging.getLogger(__name__)

# Configuration for where hashes are stored in frontmatter
HASH_NAMESPACE = '_system'
HASH_KEY = 'hashes'
CONTENT_HASH_KEY = 'content'
YAML_HASH_KEY = 'yaml'

class ActionType(Enum):
    """Enum representing the action to take based on change detection."""
    SKIP = auto()
    FULL_TRANSLATION = auto()
    YAML_UPDATE = auto()

@dataclass
class ChangeDetectionResult:
    """Data class holding the results of hash comparison."""
    content_changed: bool
    yaml_changed: bool
    old_hashes: Optional[Dict[str, str]] = None
    new_hashes: Optional[Dict[str, str]] = None

    @property
    def hashes_match(self) -> bool:
        """Return True if neither content nor YAML hashes have changed."""
        return not self.content_changed and not self.yaml_changed

def compare_hashes(
    current_hashes: Dict[str, str],
    frontmatter: Optional[Dict[str, Any]]
) -> ChangeDetectionResult:
    """
    Compare calculated hashes with stored hashes in frontmatter.

    Args:
        current_hashes: Dictionary containing newly calculated {'content': hash, 'yaml': hash}.
        frontmatter: The parsed frontmatter dictionary from the source file.

    Returns:
        ChangeDetectionResult: An object detailing the comparison outcome.
    """
    logger.debug("Comparing current hashes with stored hashes.")

    stored_hashes: Dict[str, str] = {}
    if frontmatter and HASH_NAMESPACE in frontmatter and HASH_KEY in frontmatter[HASH_NAMESPACE]:
        stored_hashes = frontmatter[HASH_NAMESPACE][HASH_KEY]
        if not isinstance(stored_hashes, dict):
            logger.warning(f"Stored hashes are not a dictionary: {stored_hashes}. Treating as missing.")
            stored_hashes = {}
    else:
        logger.debug("No stored hashes found in frontmatter.")

    current_content_hash = current_hashes.get(CONTENT_HASH_KEY)
    current_yaml_hash = current_hashes.get(YAML_HASH_KEY)

    stored_content_hash = stored_hashes.get(CONTENT_HASH_KEY)
    stored_yaml_hash = stored_hashes.get(YAML_HASH_KEY)

    # Treat missing hashes (current or stored) as a change
    content_changed = current_content_hash != stored_content_hash
    yaml_changed = current_yaml_hash != stored_yaml_hash

    logger.debug(f"Content hash comparison: Stored='{stored_content_hash}', Current='{current_content_hash}', Changed={content_changed}")
    logger.debug(f"YAML hash comparison: Stored='{stored_yaml_hash}', Current='{current_yaml_hash}', Changed={yaml_changed}")

    return ChangeDetectionResult(
        content_changed=content_changed,
        yaml_changed=yaml_changed,
        old_hashes=stored_hashes if stored_hashes else {},
        new_hashes=current_hashes
    )

def determine_action(result: ChangeDetectionResult) -> ActionType:
    """
    Determine the appropriate action based on hash comparison results.

    Args:
        result: The ChangeDetectionResult object from compare_hashes.

    Returns:
        ActionType: The action to take (SKIP, FULL_TRANSLATION, YAML_UPDATE).
    """
    action: ActionType
    reason: str

    if result.hashes_match:
        action = ActionType.SKIP
        reason = "Hashes match"
    elif result.content_changed:
        action = ActionType.FULL_TRANSLATION
        reason = "Content hash changed"
    elif result.yaml_changed:
        action = ActionType.YAML_UPDATE
        reason = "YAML hash changed, content hash matches"
    else:
        # This case should technically not be reached if logic is sound
        logger.warning("Unexpected state in determine_action. Defaulting to FULL_TRANSLATION.")
        action = ActionType.FULL_TRANSLATION
        reason = "Unexpected comparison result"

    log_message = (
        f"Change Detection Result - Action: {action.name}. Reason: {reason}. "
        f"Old Content Hash: {result.old_hashes.get(CONTENT_HASH_KEY, 'N/A')}, "
        f"New Content Hash: {result.new_hashes.get(CONTENT_HASH_KEY, 'N/A')}. "
        f"Old YAML Hash: {result.old_hashes.get(YAML_HASH_KEY, 'N/A')}, "
        f"New YAML Hash: {result.new_hashes.get(YAML_HASH_KEY, 'N/A')}."
    )
    logger.info(log_message)

    if action == ActionType.SKIP:
        logger.debug(f"Detailed comparison: Content Match={not result.content_changed}, YAML Match={not result.yaml_changed}")
    elif action == ActionType.FULL_TRANSLATION:
        logger.debug(f"Content change detected. Old: {result.old_hashes.get(CONTENT_HASH_KEY)}, New: {result.new_hashes.get(CONTENT_HASH_KEY)}")
        if result.yaml_changed:
            logger.debug(f"YAML change also detected (overridden by content change). Old: {result.old_hashes.get(YAML_HASH_KEY)}, New: {result.new_hashes.get(YAML_HASH_KEY)}")
    elif action == ActionType.YAML_UPDATE:
        logger.debug(f"YAML-only change detected. Old: {result.old_hashes.get(YAML_HASH_KEY)}, New: {result.new_hashes.get(YAML_HASH_KEY)}")
        logger.debug(f"Content hash matched. Hash: {result.new_hashes.get(CONTENT_HASH_KEY)}")

    return action 