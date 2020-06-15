package org.picar.server;

import org.picar.server.ChannelRegisterHandler.ChannelPairs;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;

public class ChannelProducer extends SimpleChannelInboundHandler<ByteBuf> {

	private static final Logger LOG = LoggerFactory.getLogger(ChannelProducer.class);
	private final ChannelPairs channelPairs;
	
	public ChannelProducer(ChannelPairs channelPairing) { this.channelPairs = channelPairing; }

	@Override
    public void channelInactive(ChannelHandlerContext ctx) {
		this.channelPairs.getProducers().remove(ctx.channel());
		LOG.info("Removed producer channel {}", ctx.channel());
	}

	@Override
	protected void channelRead0(ChannelHandlerContext ctx, ByteBuf msg) {
		this.channelPairs.getConsumers().forEach(channel -> {
			if (channel.isActive()) { channel.writeAndFlush(msg.retain()); }
		});		
	}
}
