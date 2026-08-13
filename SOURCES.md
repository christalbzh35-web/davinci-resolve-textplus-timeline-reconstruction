# Technical sources

## Documentation and standards

- **OpenTimelineIO - Academy Software Foundation**  
  https://opentimelineio.readthedocs.io/en/latest/  
  Relevance: editorial interchange model, timeline representation and adapters.

- **DaVinci Resolve Scripting API - Blackmagic Design**  
  Primary API reference. The publication should point to the documentation matching the targeted Resolve version.

## Community projects

- **AutoSubs - Thomas Moroney**  
  https://github.com/tmoroney/auto-subs/blob/main/Resolve-Integration/README.md  
  Relevance: Resolve integration using a `caption-bin.drb` containing a Fusion Text/Text+ clip.

- **Resolve OpenCaptions - David C.**  
  https://github.com/david-ca6/Resolve-OpenCaptions  
  Relevance: Text+ generation from templates stored in the Media Pool.

- **davinci-resolve-mcp - Mateo Khalil**  
  https://github.com/mateo-khalil/davinci-resolve-mcp  
  Relevance: bridge running inside Resolve Free with file-based request/response communication.

## Experimental provenance

The carrier/Text+ mechanism, the observed 24/25 fps timing behavior and timeline-context propagation come from development and qualification of the IMS/DaVinci Resolve V10 bridge.
