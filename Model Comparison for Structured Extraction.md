This is the result of asking OLMoE to extract these criteria from the spec sheet text in [Cadiant Dynamic Skylight w-Lutron Athena Spec Sheet.txt](./data/spec_sheets_text/indoor/Cadiant%20Dynamic%20Skylight%20w-Lutron%20Athena%20Spec%20Sheet.txt). This was done with the [structured_specs.py](./scripts/structured_specs.py) script.
```json
{
  "product_name": "Envision LED Smart Light",
  "specs": {
    "Lumen Output": "900 lumens",
    "Power Factor": "0.3",
    "Color Temperature": "3000K",
    "Safety Classification": "Class I",
    "IK Rating": "32",
    "Surge Protection": "125/250V, 15kA, 10/30ms",
    "Voltage": "120V",
    "LED Driver": "DC-powered, 12V",
    "Materials and Finishing": "Aluminum alloy, glass lens",
    "Dimensions / Cut-out": "6.5 inches diameter, 1.75 inches depth",
    "Certifications": ["UL Recognized", "CE Mark", "DEEPER Approved"],
    "THD": "0.25",
    "Wattage": "12 watts",
    "SDCM": "2%",
    "Lifetime": "50,000 hours",
    "Mounting Type": "Ceiling mount",
    "UGR": "18.3",
    "Flickering": "No",
    "Efficacy": "90 lumens per watt",
    "CRI": "75",
    "Operation Temperature": "0 to 40°C (32 to 104°F)",
    "IP Rating": " IP20 ",
    "Optics": "Reflector design",
    "Warranty": "2-year limited warranty"
  }
}
```
This is the result using Gemini 2.0 Flash Thinking for the same task:

```json
{
  "product_name": "Cadiant® Experience 2' x 2' Architectural LED Dynamic Skylight",
  "specs": {
    "Lumen Output": "150-6,980 Lumens",
    "Power Factor": "> 90% at full load",
    "Color Temperature": "Adjustable from 3000K to 6500K",
    "Safety Classification": "cULus Listed, Suitable for damp locations, Designed for indoor use only",
    "IK Rating": "UNK",
    "Surge Protection": "UNK",
    "Voltage": "120-277 VAC",
    "LED Driver": "Utilizes three Athena nodes and a DALI2 drivers",
    "Materials and Finishing": "Durable 22 ga. galvanized steel housing, post-painted for enhanced matte finish",
    "Dimensions / Cut-out": "Designed for use in most ceiling grids including standard 1 ½\", 9/16\", 15/16\" and hard ceiling, 23.7\" (602mm) x 23.7\" (602mm)",
    "Certifications": [
      "cULus Listed",
      "RoHS compliant",
      "Meets FCC Part 15, Subpart B, Class A limits for conducted and radiated emissions",
      "Meets the requirements of BAA and/or BABA"
    ],
    "THD": "< 20% at full load",
    "Wattage": "5-96 watts",
    "SDCM": "UNK",
    "Lifetime": "> 100,000 hours at 35˚C",
    "Mounting Type": "Designed for use in most ceiling grids",
    "UGR": "UNK",
    "Flickering": "UNK",
    "Efficacy": "Up to 83 LPW",
    "CRI": "90+ CRI",
    "Operation Temperature": "0˚C - + 35˚C (32˚F - + 95˚F)",
    "IP Rating": "Suitable for damp locations",
    "Optics": "Optimized smooth acrylic lens, Dynamic lighting via Athena programming, Soft blue-sky w/east to west sun panels",
    "Warranty": "5 years for luminaire and Lutron Athena controls; 1 year for luminaire accessories"
  }
}
```

Both models were asked to use "UNK" when they could not determine a spec. Only Gemini followed this instruction. Overall, Gemini performed well. However, the much smaller OLMoE model struggled given the same text to work with. It invented most of the specs. While the current RAG-based chatbot model uses embeddings over the text instead of structured data, OLMoE's poor performance on this information extraction task means the selection of foundation model may be a significant contributor towards the chatbot's tendency to invent fake specs.

It would be worth swapping in a larger model as the underlying LLM and testing whether that yielded improvements in information reliability.

It may also be viable to consider using a larger model for one-time information extraction and feeding reliable structured information to a smaller LLM like OLMoE for generation.