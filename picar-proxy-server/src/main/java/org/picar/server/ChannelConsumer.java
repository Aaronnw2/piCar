package org.picar.server;

import org.picar.server.ChannelRegisterHandler.ChannelPairs;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;

public class ChannelConsumer extends ChannelInboundHandlerAdapter {

	private static final Logger LOG = LoggerFactory.getLogger(ChannelConsumer.class);
	private final ChannelPairs channelPairs;
	
	public ChannelConsumer(ChannelPairs channelPairing) {
		this.channelPairs = channelPairing;
	}
	
	@Override
    public void channelInactive(ChannelHandlerContext ctx) {
		this.channelPairs.getConsumers().remove(ctx.channel());
		LOG.info("Removed consumer channel {}", ctx.channel());
	}
}
