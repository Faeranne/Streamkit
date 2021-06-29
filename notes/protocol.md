# Command and Control Protocol

Message is a json obect containing the following:

target: (double) The serial of the target machine.  if 0, broadcast.
source: (double) Serial of the sending machine.
nonce: (byte)  An incrementing message nonce, so that message retries can be matched
command: (byte)  A string indicating the command
arguments: (arbitrary length) an ordered array of arguments dependent on the command.
timestamp: (double) A unix timestamp of when the packet was sent.

This object should allow for turning everything into a single packet later.  would make the protocol super light.

details for each command follow:

`ping` 1: A simple heartbeat ping to verify the device is online.  Can also verify roundtrip latency of c&c.
`ack` 0: A command acknolagement.  Must have the same nonce as the command it acknolages.  should only be sent after the command in question is completed.
`error` 2: Indicates and error occured at the source.  If responding to a failed command, it must contain the nonce of the original command.  Otherwise, it must contain a unique nonce.
`fetch_info` 3: requests the target send it's current config info.
`info` 4: A reply to fetch_info or module_info. should contain the config details.  each info reply should contain module information for a particular module.  any module not reported should be assumed not available.
`module_info` 5: Request the target send the config for a particular module.  
`enable_module` 6: Enable a module.  first argument should be the module id, but further ones can be module dependent.
`set_module` 7: Change module settings.  arguments match enable_module
`start_stream` 8: Request the target begin a given stream.  Arguments should be module id, followed by stream id.  a third argument, destination, can be used to override the default destination.  Some streams are to files, and will not result in a new udp stream.
`stream_started` 9: Sent only when a module starts a stream of it's own volition.  should contain the same arguments as start_stream.
`stop_stream` 10: Request the target end a given stream.  Arguments should be module id, followed by stream id.
`stream_ended` 11: Sent only when a module ends a stream of it's own volition.  should contain the same arguments as end_stream.  If an error caused the stream to end, an error command should be sent seperatly.
