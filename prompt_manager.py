"""Prompt management for literary analysis experiments."""

from typing import Dict, Any, Optional


class PromptManager:
    """統一的なプロンプト管理を提供するクラス。"""

    @staticmethod
    def get_prompt(model_type: str, persona_id: str, text_content: str, model_id: str = None) -> Dict[str, Any]:
        """
        指定されたモデルタイプとペルソナに対応するプロンプトを生成します。

        Args:
            model_type: モデルタイプ（"openai", "claude", "gemini", "grok"など）
            persona_id: ペルソナID（"p1", "p2", "p3", "p4"）
            text_content: 分析対象のテキスト
            model_id: 特定のモデルID（オプション）

        Returns:
            Dict[str, Any]: モデル固有のフォーマットに変換されたプロンプト
        """
        base = PromptManager._get_base_prompt(text_content)
        system = PromptManager._get_system_prompt(persona_id)
        return PromptManager._adapt_for_model(model_type, base, system, model_id)
    
    @staticmethod
    def _get_base_prompt(text_content: str) -> str:
        """ベースプロンプトにテキストを組み込んで取得します。"""
        from parameters import BASE_PROMPT
        return BASE_PROMPT.format(text_content=text_content)
    
    @staticmethod
    def _get_system_prompt(persona_id: str) -> str:
        """指定されたペルソナのシステムプロンプトを取得します。"""
        from parameters import SYSTEM_PROMPTS
        return SYSTEM_PROMPTS[persona_id]
    
    @staticmethod
    def _adapt_for_model(
        model_type: str,
        base: str,
        system: str,
        model_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        モデル固有のフォーマットにプロンプトを変換します。

        Args:
            model_type: モデルタイプ
            base: ベースプロンプト
            system: システムプロンプト
            model_id: 特定のモデルID（オプション）

        Returns:
            Dict[str, Any]: モデル固有のフォーマットに変換されたプロンプト
        """
        from parameters import MODEL_CONFIGS
        
        config = MODEL_CONFIGS[model_type]
        model_config = config.get(model_id, config["standard"])
        
        match model_config["format"]:
            case "messages":
                # OpenAI標準フォーマット
                return {
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": base}
                    ]
                }
            case "combined":
                # OpenAI o1-miniなど、system roleをサポートしないモデル用
                return {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{system}\n\n{base}"
                        }
                    ]
                }
            case "content":
                # Claude形式
                return {
                    "system": [{"type": "text", "text": system}],
                    "messages": [{
                        "role": "user",
                        "content": [{"type": "text", "text": base}]
                    }]
                }
            case format_type:
                raise ValueError(f"Unsupported format type: {format_type}")
