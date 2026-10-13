"""Local LLM support: schema-constrained command proposals from Ollama or llama-server.

The model only proposes JSON. The interpreter validates every proposal against
the parameter registry, and the user must confirm it before it is applied.
"""
