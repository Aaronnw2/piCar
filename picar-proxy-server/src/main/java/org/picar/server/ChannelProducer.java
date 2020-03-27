package org.picar.server;

import org.picar.server.ChannelRegisterHandler.ChannelPairs;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;

public class ChannelProducer extends ChannelInboundHandlerAdapter {

	private static final Logger LOG = LoggerFactory.getLogger(ChannelProducer.class);
	private final ChannelPairs channelPairs;
	
	public ChannelProducer(ChannelPairs channelPairing) { this.channelPairs = channelPairing; }

	@Override
	public void channelRead(ChannelHandlerContext ctx, Object msg) {
		this.channelPairs.getConsumers().forEach(channel -> channel.writeAndFlush(msg));
	}
	
	@Override
    public void channelInactive(ChannelHandlerContext ctx) {
		this.channelPairs.getProducers().remove(ctx.channel());
		LOG.info("Removed producer channel {}", ctx.channel());
	}
}
